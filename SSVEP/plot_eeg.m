i = 1;
window_length = 1024;
for period = 1:16
    figure
    hold on
    [pxx, f] = periodogram(Data.EEG(((window_length * int32(period-1)):int32(window_length*period) - 1) + 1, i), rectwin(window_length), window_length, 512);
    plot(f((f>5) & (f<10)), pxx((f>5) & (f<10)), 'DisplayName', 'period=' + string(period))
    hold off
    legend
end

