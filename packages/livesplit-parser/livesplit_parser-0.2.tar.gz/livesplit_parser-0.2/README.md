# Livesplit-Parser

#### A Python Package to Parse Your Data Regarding Your Speedruns

This Pyton package parses LiveSplit files and parses data within LiveSplit files.

Install this package with `pip install livesplit_parser`

Check out the documentation for this package [here](https://trevorbushnell.github.io/livesplit_parser/).


## Example Usage

```python
from livesplit_parser import LivesplitData

lss_path = '' # put the path to your .lss file here
my_run = LivesplitData(lss_path)

print('NUMBER OF ATTEMPTS:', my_run.num_attempts)
print('NUMBER OF COMPLETED ATTEMPTS:', my_run.num_completed_attempts)
print('PERCENTAGE OF RUNS COMPLETED:', my_run.percent_runs_completed)
print('YOUR ATTEMPT DATA\n:', my_run.attempt_info_df)
print('YOUR SPLIT DATA:\n', my_run.split_info_df)
```

## TODO Features to Include

- [x] Include a `StandDev` column in the `split_info_df` that includes the standard deviation of all your attempts for that split
- [ ] Plot split time distributions using *violinplots*
- [ ] Plot runtime distributions with the splits on the x-axis and standard deviation on the y-axis
- [ ] Plot number of runs that reset between completed runs
- [ ] Plot completed runs over time (run ID on x-axis, final time on y-axis)
- [ ] Plot completed runs with a heatmap showing how good that segment was for that run
- [ ] Create a Runner class that contains a list of Runners with their data and methods that plot runs against each other
	* example: plot each runner's PB over time (runners can compare themselves against each other)
	* another example: heatmap from before with splits on the x-axis, runner on the y-axis, and heatmap comparing that segment with the means of the personal bests of every runner included

Other ideas for plots and features can be submitted to the [Issues board](https://github.com/TrevorBushnell/livesplit_parser/issues) on my GitHub repo :)
