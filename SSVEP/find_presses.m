target_frequencies = [6, 6.5, 7, 7.5, 8.2, 9.3, 10];
fs = 512;
test_times = linspace(0.5, 16, 32);
test_signal_time = 2;
test_signal_length = fs*test_signal_time;
idx_target_frequencies = int32(target_frequencies*10 + 1);
idx_target_frequencies = cat(1, idx_target_frequencies - 1, idx_target_frequencies, idx_target_frequencies + 1);
idx_target_frequencies = sort(idx_target_frequencies);


freq_pressed = [];
for subject_i = 1:5
    for trial_j = 1:2
        freq_pressed_subject = [];
        load('./multi/Sub' + string(subject_i) + '_' + string(trial_j) + '_multitarget.mat')
        for test_time_i = test_times
            freq_pressed_trial = [];
            test_end = test_time_i * fs;
            test_start = max(test_end - test_signal_length + 1, 1);
            test_timestamps = test_start:test_end;
            test_max_power = zeros(length(target_frequencies), 1);
            for channel = 1:10
                [pxx, f] = periodogram(Data.EEG(test_timestamps, channel), rectwin(length(test_timestamps)), fs*10 , fs);
                relevant_pxx_separate = pxx(idx_target_frequencies);
                relevant_pxx = zeros(length(target_frequencies), 1);
                for i=1:length(target_frequencies)
                    relevant_pxx(i) = sum(relevant_pxx_separate((1 + 3*(i-1)):(3*i)));
                end
                [max_power, idx_max_power] = max(relevant_pxx);
                normalized_pxx = relevant_pxx/max_power;
                if (sum(normalized_pxx) - 1) < 0.5*(length(relevant_pxx) - 1)
                    test_max_power(idx_max_power) = test_max_power(idx_max_power) + 1;
                end
            end
            [max_count, idx_max_count]  = max(test_max_power);
            if max_count > 5
                freq_pressed_trial = cat(1, freq_pressed_trial, target_frequencies(idx_max_count));
            else
                freq_pressed_trial = cat(1, freq_pressed_trial, "None");
            end
        end
        freq_pressed_subject =  cat(1, freq_pressed_subject, freq_pressed_trial);
    end
    freq_pressed = cat(1, freq_pressed, freq_pressed_subject);
end