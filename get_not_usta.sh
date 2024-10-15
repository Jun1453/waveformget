#!/opt/bin/fish
conda activate waveformget
for year in (seq 2012 2023)
    python mass_download.py $year not_usta
end
