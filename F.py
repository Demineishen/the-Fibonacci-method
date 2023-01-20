from matplotlib import pyplot as plt
import matplotlib.animation as animation
import numpy as np
from tkinter import *
from tkinter import messagebox as mbox

def F1(x):
    return (x - 3)**2


def F2(x):
    return np.sin(x**2) + np.cos(x**2)


def F3(x):
    return 3 - x**3

def iterations(n):
    if (n < 1):
        return 0
    f0 = 1
    f1 = 1
    fn = f1 + f0
    counter = 2
    while fn < n:
        f0 = f1
        f1 = fn
        fn = f0 + f1
        counter += 1
    return counter


def Fib(itrs):
    f0 = 1
    f1 = 1
    fn = f1 + f0
    k = 2
    while k <= itrs:
        f0 = f1
        f1 = fn
        fn = f0 + f1
        k += 1
    return fn

#Интерфейс
def interface():
    fig, ax = plt.subplots()
    rx = []
    ry = []
    bx = []
    by = []
    gx = []
    gy = []
    window = Tk()
    window.title("Оптимизация")
    window.geometry('600x600')
    name = Label(window, text="Метод Фибоначчи", font=("Arial", 14))
    lbl = Label(window, text="Выберите функцию: ", anchor=W)
    name.place(x = 210, y = 0)
    lbl.place(x = 0, y = 15)
    
    #Выбор функции
    choice = IntVar()
    choice.set(1)
    func1 = Radiobutton(window, text='(x - 3)^2', variable=choice, value=1)
    func1.place(x = 0, y = 40)
    func2 = Radiobutton(window, text='sinx^2 + cosx^2', variable=choice, value=2)
    func2.place(x = 0, y = 70)
    func3 = Radiobutton(window, text='3 - x^3', variable=choice, value=3)
    func3.place(x = 0, y = 100)
    
    #Выбор пользователя искать максимум или минимум
    action = Label(window, text="Выберите действие:")
    action.place(x = 0, y = 150)
    min_max_choice = IntVar()
    min_max_choice.set(1)
    button_min = Radiobutton(window, text='Найти точку минимума', variable=min_max_choice, value=1)
    button_max = Radiobutton(window, text='Найти точку максимума', variable=min_max_choice, value=2)
    button_max.place(x = 0, y = 180, height=12)
    button_min.place(x = 0, y = 210, height = 12)
    
    #Ввод данных
    data = Label(window, text="Введите данные:")
    data.place(x = 0, y = 260)
    a_label = Label(window, text='Начало отрезка:')
    a_label.place(x = 0, y = 290)
    a_entry = Entry(window)
    a_entry.insert(0, 2)
    a_entry.place(x = 100, y = 290)

    b_label = Label(window, text='Конец отрезка:')
    b_label.place(x = 0, y = 320)
    b_entry = Entry(window)
    b_entry.insert(0, 5)
    b_entry.place(x = 100, y = 320)
    
    eps_label = Label(window, text='Точность:')
    eps_label.place(x = 0, y = 350)
    eps_entry = Entry(window)
    eps_entry.insert(0, 0.001)
    eps_entry.place(x = 100, y = 350)
    
    #Нахождение минимума
    def solve_min(f):
        a = float(a_entry.get())
        b = float(b_entry.get())
        eps = float(eps_entry.get())
        n = (b - a) / eps
        iters = iterations(n)
        k = 1
        xmin = (a + b) / 2
        while k <= iters:
            x1 = a + ((b - a) * Fib(iters - k - 1)) / Fib(iters - k + 1)
            x2 = a + ((b - a) * Fib(iters - k)) / Fib(iters - k + 1)
            y1 = f(x1)
            y2 = f(x2)
            if y1 <= y2:
                b = x2
            else:
                a = x1
            k += 1
            xmin = (a + b) / 2
            rx.append(xmin)
            ry.append(f(xmin))
        return xmin
    
    #Нахождение максимума
    def solve_max(f):
        a = float(a_entry.get())
        b = float(b_entry.get())
        eps = float(eps_entry.get())
        n = (b - a) / eps
        iters = iterations(n)
        k = 1
        xmax = (a + b) / 2
        while k <= iters:
            x1 = a + ((b - a) * Fib(iters - k - 1)) / Fib(iters - k + 1)
            x2 = a + ((b - a) * Fib(iters - k)) / Fib(iters - k + 1)
            y1 = -f(x1)
            y2 = -f(x2)
            if y1 <= y2:
                b = x2
            else:
                a = x1
            k += 1
            xmax = (a + b) / 2
            rx.append(xmax)
            ry.append(f(xmax))
        return xmax
    
    #Проверка на ошибки
    def check():
        flag = False
        if a_entry.get().isalpha() or b_entry.get().isalpha() or eps_entry.get().isalpha():
            flag = True
            mbox.showerror("Ошибка", "Неверный тип данных")
        elif float(eps_entry.get()) == 0 or float(eps_entry.get()) > 0.1:
            flag = True
            mbox.showerror("Ошибка", "Точность не может быть больше 0.1 и не может быть равна 0")
        elif float(a_entry.get()) == float(b_entry.get()):
            flag = True
            mbox.showerror("Ошибка", "Границы должны различаться")
        elif float(a_entry.get()) > float(b_entry.get()):
            flag = True
            mbox.showerror("Ошибка", "Начало границы должна быть меньше конца границы")
        return flag
    
    #Очистка точек
    def clear_dots():
        bx.clear()
        by.clear()
        gx.clear()
        gy.clear()
        rx.clear()
        ry.clear()
    
    #Команда для кнопки "Решить"    
    def solve_button():
        clear_dots()
        if choice.get() == 1:
            f = F1
        elif choice.get() == 2:
            f = F2
        elif choice.get() == 3:
            f = F3
        if min_max_choice.get() == 1:
            if not check():
                result = solve_min(f)
                answer_label = Label(window, text = f"Ответ: {result}", relief = GROOVE)
                answer_label.place(x = 0, y = 380)
        elif min_max_choice.get() == 2:
            if not check():
                result = solve_max(f)
                answer_label = Label(window, text = f"Ответ: {result}", relief = GROOVE)
                answer_label.place(x = 0, y = 380)
        return 0
            
    #Кнопка "Решить"
    solution = Button(window, command=solve_button, text='Решить', width=15)
    solution.place(x = 210, y = 400)
    
 
    #Команда для кнопки "Показать график"
    def graph():
        #if len(rx) == 0:
            #mbox.showerror("Ошибка", "График не может быть показан, так как нет точек минимума/максимума")
        #else:        
        clear_dots()
        ax.clear()
        a = float(a_entry.get())
        b = float(b_entry.get())
        if a == b:
            mbox.showerror("Ошибка", "График не может быть показан, так как начало границы равно её концу")
        elif a > b:
            mbox.showerror("Ошибка", "График не может быть показан, так как начало границы больше её конца")
        else:
            t = np.linspace(a, b, 200)
            f = 0
            if choice.get() == 1:
                    f = F1
                    s = f(t)
                    l = plt.plot(t, s)
            elif choice.get() == 2:
                    f = F2
                    s = f(t)
                    l = plt.plot(t, s)
            elif choice.get() == 3:
                    f = F3
                    s = f(t)
                    l = plt.plot(t, s)
            
            if min_max_choice.get() == 1:
                    min_x = solve_min(f)
                    plt.xlabel('Минимум')
                    plt.ylabel('Значение при минимуме')
                    redDot, = plt.plot(0, f(0), 'ro', label='Минимум')
                    plt.title(f'Найденный минимум: {min_x}, значение при минимуме: {f(min_x)}')
            elif min_max_choice.get() == 2:
                    max_x = solve_max(f)
                    plt.xlabel('Максимум')
                    plt.ylabel('Значение при максимуме')
                    redDot, = plt.plot(0, f(0), 'ro', label='Максимум')   
                    plt.title(f'Найденный максимум: {max_x}, значение при максимуме: {f(max_x)}')
                    
            begin = plt.plot(a, f(a), 'wo', label = f'Заданное начало границы: {a}') 
            end = plt.plot(b, f(b), 'wo', label=f'Заданный конец границы: {b}')    
            blueDot, = plt.plot(a, f(a), 'bo', label='Начало отрезка')
            greenDot, = plt.plot(b, f(b), 'go', label='Конец отрезка')
            
            def animate_red(i):
                    redDot.set_xdata(rx[:i])
                    redDot.set_ydata(ry[:i])
                    return redDot,
                
            blueDot, = plt.plot(bx, by, 'bo')
            greenDot, = plt.plot(gx, gy, 'go')
            animate = animation.FuncAnimation(fig, animate_red, frames=len(rx), interval=1000, blit=True)
                    
            plt.legend()
            plt.show()

    #Кнопка "Показать график"
    show = Button(window, command=graph, text='Показать график', width=15)
    show.place(x = 210, y = 430)
    #window.mainloop()
    
    #Кнопка "Выход"
    qt = Button(window, command = window.quit, text = 'Выход')
    qt.place(x = 244, y = 460)
    window.mainloop()
def main():
    interface()

if __name__ == '__main__':
    main()
