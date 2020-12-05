fs = 512;
target_frequencies = [6, 6.5, 7, 7.5, 8.2, 9.3, 10];
target_frequencies = cat(2, target_frequencies, 2*target_frequencies);
f_sampling = linspace(0, 256, 2561);
f_relevant = (f_sampling > 5) & (f_sampling <21);
for subject_i = 1:4
    figure
    load('./single/Sub' + string(subject_i) + '_singletarget.mat');
    [pxx, f] = periodogram(Data.EEG, rectwin(length(Data.EEG)), fs*10 , fs);
    hold on
    list_plots = [];
    for trial_i = 1:21
        list_plots = cat(1, list_plots, plot(f(f_relevant), pxx(f_relevant, trial_i), 'DisplayName', 'Trial ' + string(trial_i)));
    end
    for i = 1:length(target_frequencies)
        xline(target_frequencies(i), '--', string(target_frequencies(i)) + "Hz", 'DisplayName', '')
    end
    legend(list_plots)
    title('PSD for Subject ' + string(subject_i))
    hold off
end


