# paperplots
Camera ready machine learning plots with a Tensorboard-like API

Ever felt like the tensorboard summary writer can do a bit more than just letting you monitor your training logs? Wouldn't it be nice if you could also directly get pretty paper-ready versions of your tensorboard logs? Paperplots does just this! 

- Record scalars in the exact same way as you do with [tensorboard summarywriter](https://pytorch.org/docs/stable/tensorboard.html) 
- Save your training data in easy to access pickle files
- Plot runs, whole experiments, and even compare different experiments
- Automatically calculate simple convenience transforms such as rolling averages and shaded error regions

[**Documentation**](Docs.md)

# Examples

## Writing Logs
```
writer = Writer(logdir=f'runs/algo', run_name=f'run1')

for i in range(iter):
	writer.add_scalar("loss", loss_value, i, ylabel="loss", xlabel="num iter", name="algo loss")

writer.close()

```

## Plotting Written Logs
```
plotter = Plotter(logdir='runs')

# Plotting runs
plotter.plot_run(run_name="algo/run1")

# Compare two runs
plotter.plot_run(run_name=["algo/run0", "algo/run1"])

# Plot an average over all runs in the experiment
plotter.plot_experiment(exp_name="algo")

# Compare two experiments
plotter.plot_experiment(exp_name=["algo1", "algo2"])
```

![Plots](test_plots/plots.png)