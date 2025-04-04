function calculateXY(t, x0, y0, L, step, V) {
    const t_row = L / V; // Время на строку
    const t_step = step / V; // Время на переход
    const t_total = t_row + t_step; // Общее время на строку и переход

    const n = Math.floor(t / t_total); // Текущая строка

    // Координата y
    const y = y0 + n * step;

    // Координата x
    const t_in_cycle = t % t_total;
    let x;
    if (n % 2 === 0) {
        // Движение слева направо
        x = x0 + t_in_cycle * V;
        
    } else {
        // Движение справа налево
        x = x0 + L - t_in_cycle * V;
    }

    return { x, y };
}

// Пример использования
const x0 = 0, y0 = 0, L = 40, step = 1, V = 10;
const t = 12.573; // Время в секундах

const { x, y } = calculateXY(t, x0, y0, L, step, V);
console.log(`x(${t}) = ${x}, y(${t}) = ${y}`);