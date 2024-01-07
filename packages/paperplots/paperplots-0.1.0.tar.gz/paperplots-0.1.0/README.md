# paperplots
Camera ready machine learning plots with a Tensorboard-like API

Ever felt like the tensorboard summary writer can do a bit more than just letting you monitor your training logs? Wouldn't it be nice if you could also directly get pretty paper-ready versions of your tensorboard logs? Paperplots does just this! 

- Record scalars in the exact same way as you do with [tensorboard summarywriter](https://pytorch.org/docs/stable/tensorboard.html) 
- Save your training data in easy to access pickle files
- Plot runs, whole experiments, and even compare different experiments
- Automatically calculate simple convenience transforms such as rolling averages and shaded error regions