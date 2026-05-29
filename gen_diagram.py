"""Генератор блок-схемы алгоритма приложения по ГОСТ 19.701-90."""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

W, H = A4          # 595 x 842 pt
ML = 40            # margin

# Шрифты с кириллицей
pdfmetrics.registerFont(TTFont("Arial",      r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialBold",  r"C:\Windows\Fonts\arialbd.ttf"))

# ─────────────────────── Примитивы ГОСТ ───────────────────────

def _text(c, x, y, w, h, txt, font="Arial", size=8):
    """Многострочный текст по центру блока."""
    c.setFont(font, size)
    lines = txt.split("\n")
    lh = size + 2
    ty = y + h / 2 + (len(lines) - 1) * lh / 2 - size * 0.3
    for line in lines:
        c.drawCentredString(x + w / 2, ty, line)
        ty -= lh

def terminal(c, x, y, w=130, h=30, txt=""):
    """Начало/Конец — скруглённый прямоугольник."""
    r = h / 2
    p = c.beginPath()
    p.moveTo(x + r, y + h)
    p.lineTo(x + w - r, y + h)
    p.arcTo(x + w - 2*r, y, x + w, y + h, 0, 90)
    p.lineTo(x + r, y)
    p.arcTo(x, y, x + 2*r, y + h, 180, 90)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    _text(c, x, y, w, h, txt, "ArialBold", 9)

def process(c, x, y, w=160, h=30, txt=""):
    """Процесс — прямоугольник."""
    c.rect(x, y, w, h)
    _text(c, x, y, w, h, txt)

def decision(c, x, y, w=160, h=40, txt=""):
    """Решение — ромб."""
    cx, cy = x + w/2, y + h/2
    p = c.beginPath()
    p.moveTo(cx, y + h)
    p.lineTo(x + w, cy)
    p.lineTo(cx, y)
    p.lineTo(x, cy)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    _text(c, x, y, w, h, txt, size=7.5)

def inout(c, x, y, w=160, h=30, txt=""):
    """Ввод/Вывод — параллелограмм."""
    d = 12
    p = c.beginPath()
    p.moveTo(x + d, y + h)
    p.lineTo(x + w, y + h)
    p.lineTo(x + w - d, y)
    p.lineTo(x, y)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    _text(c, x, y, w, h, txt)

def predef(c, x, y, w=160, h=30, txt=""):
    """Предопределённый процесс — прямоугольник с вертикальными полосами."""
    c.rect(x, y, w, h)
    c.line(x + 10, y, x + 10, y + h)
    c.line(x + w - 10, y, x + w - 10, y + h)
    _text(c, x, y, w, h, txt)

def arrow(c, x1, y1, x2, y2):
    """Стрелка."""
    c.line(x1, y1, x2, y2)
    # наконечник
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    aw = 6
    for da in (0.4, -0.4):
        c.line(x2, y2,
               x2 - aw * math.cos(angle + da),
               y2 - aw * math.sin(angle + da))

def label(c, x, y, txt, size=7):
    c.setFont("Arial", size)
    c.drawString(x, y, txt)


# ═══════════════════════ СТРАНИЦА 1: Авторизация ═══════════════════════

def page1(c):
    c.setLineWidth(0.8)
    c.setStrokeColor(colors.black)

    BW = 180   # block width
    BH = 30    # block height
    DH = 44    # decision height
    CX = W / 2 - BW / 2   # left edge so block is centred

    # Сетка Y сверху вниз
    y = H - 60
    GAP = 18

    # Заголовок
    c.setFont("ArialBold", 11)
    c.drawCentredString(W/2, H - 30, "Алгоритм работы приложения «Магазин обуви»")
    c.setFont("Arial", 9)
    c.drawCentredString(W/2, H - 44, "Лист 1: Запуск и авторизация")
    c.line(ML, H-50, W-ML, H-50)

    # 1. НАЧАЛО
    y -= BH
    y1_start = y
    terminal(c, CX, y, BW, BH, "НАЧАЛО")
    cy = y

    # стрелка
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)
    cy = y

    # 2. Запуск приложения
    y -= BH
    process(c, CX, y, BW, BH, "Запуск приложения")
    cy = y
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)
    cy = y

    # 3. Отображение окна авторизации
    y -= BH
    process(c, CX, y, BW, BH, "Отображение окна авторизации")
    cy = y
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)
    cy = y

    # 4. Ввод данных
    y -= BH
    inout(c, CX, y, BW, BH, "Ввод логина и пароля\nпользователем")
    cy_input = y   # точка входа — нужна для цикла
    cy = y
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+DH)
    cy = y

    # 5. Гостевой вход?
    y -= DH
    decision(c, CX, y, BW, DH, "Нажата кнопка\n«Войти как гость»?")
    dec5_y = y
    cy = y
    # Да → вправо → к блоку «Роль = Гость»
    rx = CX + BW + 20
    ry = y + DH/2 - BH/2
    arrow(c, CX+BW, y+DH/2, rx, y+DH/2)
    label(c, CX+BW+3, y+DH/2+3, "Да")
    process(c, rx, ry, 100, BH, "Роль = Гость")
    # стрелка от «Роль = Гость» вниз на несколько шагов — соединим позже
    role_guest_x = rx + 50
    role_guest_y = ry

    # Нет → вниз
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)
    label(c, CX+BW/2+3, cy-GAP/2, "Нет")
    cy = y

    # 6. Поля заполнены?
    y -= DH
    decision(c, CX, y, BW, DH, "Логин и пароль\nзаполнены?")
    dec6_y = y
    cy = y
    # Нет → влево → «Вывод ошибки»
    lx = CX - 130
    ly = y + DH/2 - BH/2
    arrow(c, CX, y+DH/2, lx+100, y+DH/2)
    label(c, CX-60, y+DH/2+3, "Нет")
    process(c, lx, ly, 120, BH, "Вывод:\n«Введите логин\nи пароль»")
    # стрелка назад к вводу — вертикально вверх
    err_cx = lx + 60
    arrow(c, err_cx, ly, err_cx, cy_input + BH/2)
    arrow(c, err_cx, cy_input + BH/2, CX, cy_input + BH/2)

    # Да → вниз
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)
    label(c, CX+BW/2+3, cy-GAP/2, "Да")
    cy = y

    # 7. Проверка в БД
    y -= BH
    predef(c, CX, y, BW, BH, "Проверка данных в БД")
    cy = y
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+DH)
    cy = y

    # 8. Пользователь найден?
    y -= DH
    decision(c, CX, y, BW, DH, "Пользователь\nнайден?")
    dec8_y = y
    cy = y
    # Нет → влево → «Пользователь не найден»
    lx2 = CX - 140
    ly2 = y + DH/2 - BH/2
    arrow(c, CX, y+DH/2, lx2+130, y+DH/2)
    label(c, CX-70, y+DH/2+3, "Нет")
    process(c, lx2, ly2, 135, BH, "Вывод:\n«Пользователь не\nнайден»")
    err2_cx = lx2 + 67
    # стрелка вверх к блоку ввода
    loop_y = cy_input - 5
    arrow(c, err2_cx, ly2, err2_cx, loop_y)
    arrow(c, err2_cx, loop_y, CX, loop_y)
    arrow(c, CX, loop_y, CX, cy_input + BH/2)

    # Да → вниз
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)
    label(c, CX+BW/2+3, cy-GAP/2, "Да")
    cy = y

    # 9. Определение роли
    y -= BH
    process(c, CX, y, BW, BH, "Определение роли\nпользователя")
    role_block_y = y
    cy = y

    # «Роль = Гость» тоже приходит сюда
    # нарисуем стрелку от блока Гость вниз и влево к этому блоку
    arrow(c, role_guest_x, role_guest_y, role_guest_x, role_block_y + BH/2)
    arrow(c, role_guest_x, role_block_y + BH/2, CX + BW, role_block_y + BH/2)

    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)
    cy = y

    # 10. Переход к гл. окну
    y -= BH
    process(c, CX, y, BW, BH, "Открытие главного окна")
    cy = y
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)

    # Метка «на лист 2»
    c.setFont("ArialBold", 8)
    c.drawCentredString(CX+BW/2, y+2, "→ Лист 2")
    c.circle(CX+BW/2, y+BH/2+4, 14, stroke=1, fill=0)

    # Рамка
    c.setLineWidth(0.5)
    c.rect(ML, ML, W-2*ML, H-2*ML)
    c.setFont("Arial", 7)
    c.drawRightString(W-ML-5, ML+5, "ГОСТ 19.701-90  |  Лист 1 из 2")


# ═══════════════════════ СТРАНИЦА 2: Главное окно ═══════════════════════

def page2(c):
    c.setLineWidth(0.8)
    c.setStrokeColor(colors.black)

    BW = 180
    BH = 30
    DH = 44
    CX = W/2 - BW/2
    GAP = 16

    c.setFont("ArialBold", 11)
    c.drawCentredString(W/2, H-30, "Алгоритм работы приложения «Магазин обуви»")
    c.setFont("Arial", 9)
    c.drawCentredString(W/2, H-44, "Лист 2: Главное окно")
    c.line(ML, H-50, W-ML, H-50)

    y = H - 75

    # Коннектор «с листа 1»
    c.circle(CX+BW/2, y, 14, stroke=1, fill=0)
    c.setFont("ArialBold", 8)
    c.drawCentredString(CX+BW/2, y-3, "Лист 1")
    y -= 14 + GAP

    # 11. Загрузка каталога
    arrow(c, CX+BW/2, y+GAP, CX+BW/2, y+BH)
    y -= BH
    process(c, CX, y, BW, BH, "Загрузка товаров из БД")
    cy = y
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)
    cy = y

    # 12. Отображение каталога
    y -= BH
    process(c, CX, y, BW, BH, "Отображение каталога товаров")
    cy = y
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+DH)
    cy = y

    # 13. Выбор действия
    y -= DH
    decision(c, CX, y, BW, DH, "Действие\nпользователя")
    main_dec_y = y
    cy = y

    # ── Ветка: Поиск/фильтр/сортировка (влево)
    lx = CX - 150
    arrow(c, CX, y+DH/2, lx+140, y+DH/2)
    label(c, CX-80, y+DH/2+3, "Поиск/\nфильтр")
    fy = y+DH/2 - BH/2
    process(c, lx, fy, 140, BH, "Применение поиска,\nфильтра, сортировки")
    arrow(c, lx+70, fy, lx+70, fy-GAP)
    predef(c, lx, fy-GAP-BH, 140, BH, "Запрос к БД\nс параметрами")
    arrow(c, lx+70, fy-GAP-BH, lx+70, fy-GAP-BH-GAP)
    process(c, lx, fy-GAP-BH-GAP-BH, 140, BH, "Обновление\nсписка товаров")
    # стрелка назад к «Отображение каталога»
    back_y = fy-GAP-BH-GAP-BH
    arrow(c, lx+140, back_y+BH/2, CX, back_y+BH/2)
    arrow(c, CX, back_y+BH/2, CX, cy+DH)

    # ── Ветка: CRUD товара (вправо)
    rx = CX + BW + 20
    arrow(c, CX+BW, y+DH*0.75, rx, y+DH*0.75)
    label(c, CX+BW+3, y+DH*0.75+3, "CRUD\nтовара")
    ty = y+DH*0.75 - BH/2
    decision(c, rx, ty-DH/2, 110, DH, "Роль =\nАдминистратор?")
    d_admin_y = ty - DH/2
    # Да → вниз
    arrow(c, rx+55, d_admin_y, rx+55, d_admin_y-GAP)
    label(c, rx+58, d_admin_y-GAP/2, "Да")
    process(c, rx, d_admin_y-GAP-BH, 110, BH, "Форма\nдобавить/редакт./удалить")
    arrow(c, rx+55, d_admin_y-GAP-BH, rx+55, d_admin_y-GAP-BH-GAP)
    predef(c, rx, d_admin_y-GAP-BH-GAP-BH, 110, BH, "Сохранение\nв БД")
    arrow(c, rx+55, d_admin_y-GAP-BH-GAP-BH, rx+55, d_admin_y-GAP-BH-GAP-BH-GAP)
    process(c, rx, d_admin_y-GAP-BH-GAP-BH-GAP-BH, 110, BH, "Обновление\nкаталога")
    # Нет → вывод
    arrow(c, rx+110, d_admin_y+DH/2, rx+130, d_admin_y+DH/2)
    label(c, rx+112, d_admin_y+DH/2+3, "Нет")
    process(c, rx+130, d_admin_y+DH/2-BH/2, 90, BH, "Нет доступа")

    # ── Ветка: Заказы (вниз)
    y -= GAP
    arrow(c, CX+BW/2, cy, CX+BW/2, y+BH)
    label(c, CX+BW/2+3, cy-GAP/2, "Заказы")
    cy = y

    y -= BH
    decision(c, CX, y, BW, DH, "Роль = Менеджер\nили Администратор?")
    dec_ord_y = y
    cy2 = y
    # Нет → влево
    arrow(c, CX, y+DH/2, CX-100, y+DH/2)
    label(c, CX-70, y+DH/2+3, "Нет")
    process(c, CX-160, y+DH/2-BH/2, 60, BH, "Нет\nдоступа")

    # Да → вниз
    y -= GAP
    arrow(c, CX+BW/2, cy2, CX+BW/2, y+BH)
    label(c, CX+BW/2+3, cy2-GAP/2, "Да")
    cy2 = y

    y -= BH
    predef(c, CX, y, BW, BH, "Загрузка заказов из БД")
    cy2 = y
    y -= GAP
    arrow(c, CX+BW/2, cy2, CX+BW/2, y+BH)
    cy2 = y

    y -= BH
    process(c, CX, y, BW, BH, "Отображение списка заказов")
    cy2 = y
    y -= GAP
    arrow(c, CX+BW/2, cy2, CX+BW/2, y+DH)
    cy2 = y

    y -= DH
    decision(c, CX, y, BW, DH, "CRUD заказа?\n(только Администратор)")
    cy2 = y
    # Да → вниз
    y -= GAP
    arrow(c, CX+BW/2, cy2, CX+BW/2, y+BH)
    label(c, CX+BW/2+3, cy2-GAP/2, "Да")
    cy2 = y

    y -= BH
    process(c, CX, y, BW, BH, "Форма заказа\n(добавить/редакт./удалить)")
    cy2 = y
    y -= GAP
    arrow(c, CX+BW/2, cy2, CX+BW/2, y+BH)
    cy2 = y

    y -= BH
    predef(c, CX, y, BW, BH, "Сохранение заказа в БД")
    cy2 = y
    y -= GAP
    arrow(c, CX+BW/2, cy2, CX+BW/2, y+BH)
    cy2 = y

    # ── Ветка: Выход
    y -= DH
    decision(c, CX, y, BW, DH, "Нажата кнопка\n«Выход»?")
    exit_y = y
    # Нет → вправо → петля назад
    arrow(c, CX+BW, y+DH/2, CX+BW+30, y+DH/2)
    label(c, CX+BW+3, y+DH/2+3, "Нет")
    arrow(c, CX+BW+30, y+DH/2, CX+BW+30, H-75-14-GAP-BH/2)
    arrow(c, CX+BW+30, H-75-14-GAP-BH/2, CX+BW, H-75-14-GAP-BH/2)
    # Да → вниз
    y -= GAP
    arrow(c, CX+BW/2, exit_y, CX+BW/2, y+BH)
    label(c, CX+BW/2+3, exit_y-GAP/2, "Да")
    cy2 = y

    y -= BH
    process(c, CX, y, BW, BH, "Закрытие главного окна\nОтображение окна авторизации")
    cy2 = y
    y -= GAP
    arrow(c, CX+BW/2, cy2, CX+BW/2, y+BH)
    cy2 = y

    y -= BH
    terminal(c, CX, y, BW, BH, "КОНЕЦ")

    c.setLineWidth(0.5)
    c.rect(ML, ML, W-2*ML, H-2*ML)
    c.setFont("Arial", 7)
    c.drawRightString(W-ML-5, ML+5, "ГОСТ 19.701-90  |  Лист 2 из 2")


# ═══════════════════════ Генерация PDF ═══════════════════════

out = "docs/algorithm.pdf"
import os; os.makedirs("docs", exist_ok=True)

c = canvas.Canvas(out, pagesize=A4)

page1(c)
c.showPage()

page2(c)
c.showPage()

c.save()
print(f"Сохранено: {out}")
