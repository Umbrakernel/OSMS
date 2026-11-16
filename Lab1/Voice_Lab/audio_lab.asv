clear
clc
close all

[y, Fs] = audioread('voice.wav');
y = mean(y, 2);

info = audioinfo('voice.wav');
N = length(y);
T = info.Duration;
t = (0:N-1)/Fs;
Fs_calc = N/T;

disp(['Частота дискретизации файла: ', num2str(Fs), ' Гц'])
disp(['Количество отсчетов: ', num2str(N)])
disp(['Длительность записи: ', num2str(T), ' с'])
disp(['Рассчитанная частота дискретизации: ', num2str(Fs_calc), ' Гц'])

figure
plot(t, y)
title('Исходный сигнал')
xlabel('Время, с')
ylabel('Амплитуда')
grid on

sound(y, Fs)
pause(T + 1)

y1 = downsample(y, 10);
Fs1 = Fs/10;
N1 = length(y1);
T1 = N1/Fs1;
t1 = (0:N1-1)/Fs1;

disp(['Новая частота дискретизации: ', num2str(Fs1), ' Гц'])
disp(['Количество отсчетов после прореживания: ', num2str(N1)])
disp(['Длительность после прореживания: ', num2str(T1), ' с'])

figure
plot(t1, y1)
title('Сигнал после уменьшения частоты дискретизации в 10 раз')
xlabel('Время, с')
ylabel('Амплитуда')
grid on

sound(y1, Fs1)
pause(T1 + 1)

Y = fft(y);
A = abs(Y/N);
A = A(1:floor(N/2)+1);
A(2:end-1) = 2*A(2:end-1);
freq = (0:floor(N/2))*Fs/N;

A_bw = A;
A_bw(1) = 0;
idx = find(A_bw > max(A_bw)*0.01);
fmin = freq(idx(1));
fmax = freq(idx(end));
width = fmax - fmin;

disp(['Минимальная заметная частота исходного сигнала: ', num2str(fmin), ' Гц'])
disp(['Максимальная заметная частота исходного сигнала: ', num2str(fmax), ' Гц'])
disp(['Ширина спектра исходного сигнала: ', num2str(width), ' Гц'])
disp(['Требуемая частота дискретизации не менее: ', num2str(2*fmax), ' Гц'])

figure
plot(freq, A)
title('Амплитудный спектр исходного сигнала')
xlabel('Угловая частота, Гц')
ylabel('Амплитуда')
grid on

Y1 = fft(y1);
A1 = abs(Y1/N1);
A1 = A1(1:floor(N1/2)+1);
A1(2:end-1) = 2*A1(2:end-1);
freq1 = (0:floor(N1/2))*Fs1/N1;

A1_bw = A1;
A1_bw(1) = 0;
idx1 = find(A1_bw > max(A1_bw)*0.01);
fmin1 = freq1(idx1(1));
fmax1 = freq1(idx1(end));
width1 = fmax1 - fmin1;

disp(['Минимальная заметная частота после прореживания: ', num2str(fmin1), ' Гц'])
disp(['Максимальная заметная частота после прореживания: ', num2str(fmax1), ' Гц'])
disp(['Ширина спектра после прореживания: ', num2str(width1), ' Гц'])

figure
plot(freq1, A1)
title('Амплитудный спектр после прореживания')
xlabel('Угловая частота, Гц')
ylabel('Амплитуда')
grid on

figure
plot(freq, A)
hold on
plot(freq1, A1)
xlim([0 Fs1/2])
title('Сравнение амплитудных спектров')
xlabel('Частота, Гц')
ylabel('Амплитуда')
legend('Исходный сигнал', 'После прореживания')
grid on

bits_list = [3 4 5 6];

for k = 1:length(bits_list)
    bits = bits_list(k);
    yq = quantize_adc(y, bits);

    err = y - yq;
    mae = mean(abs(err));
    mse = mean(err.^2);

    disp(['Разрядность АЦП: ', num2str(bits), ' бит'])
    disp(['Средняя абсолютная ошибка: ', num2str(mae)])
    disp(['Среднеквадратичная ошибка: ', num2str(mse)])

    Yq = fft(yq);
    Aq = abs(Yq/N);
    Aq = Aq(1:floor(N/2)+1);
    Aq(2:end-1) = 2*Aq(2:end-1);

    figure
    plot(t, y)
    hold on
    plot(t, yq)
    title(['Квантование сигнала, ', num2str(bits), ' бит'])
    xlabel('Время, с')
    ylabel('Амплитуда')
    legend('Исходный сигнал', 'Квантованный сигнал')
    grid on

    figure
    plot(freq, A)
    hold on
    plot(freq, Aq)
    title(['Амплитудные спектры, ', num2str(bits), ' бит'])
    xlabel('Угловая частота, Гц')
    ylabel('Амплитуда')
    legend('Исходный сигнал', 'Квантованный сигнал')
    grid on
end

function yq = quantize_adc(y, bits)
levels = 2^bits;
step = 2/(levels-1);
yq = round((y+1)/step)*step-1;
yq = max(yq, -1);
yq = min(yq, 1);
end
