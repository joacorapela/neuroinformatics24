# Neuroinformatics for SWC PhD students 2024 repository (under construction)

- <a name="lecturesSchedule"></a>lectures schedule:

    | Week | Date  | Topic | Lecturers | Type |
    |------|-------|-------|-----------|------|
    | 01 | Jan 11 | [The t-test and randomization tests](https://github.com/joacorapela/neuroinformatics24/blob/master/practicals/01_tTestAndRandomizationTests/introAndHipothesisTests.pdf) | [Joaquin Rapela](https://www.gatsby.ucl.ac.uk/~rapela) | practical |
    | 02 | Jan 18 | [Power spectra](https://github.com/joacorapela/neuroinformatics24/blob/master/practicals/02_LFPs_spectralAnalysis/spectralAnalysis.pdf) | [Joaquin Rapela](https://www.gatsby.ucl.ac.uk/~rapela) [Yousef Mohammadi](y.mohammadi@ucl.ac.uk) [Joe Ziminski](https://www.sainsburywellcome.org/web/people/joe-ziminski)| practical |
    | 03 | Jan 25 | [Spectrogram and coherence](https://github.com/joacorapela/neuroinformatics24/blob/master/practicals/03_spectralAnalysisForNonStationarySignals) | [Joaquin Rapela](https://www.gatsby.ucl.ac.uk/~rapela) [Yousef Mohammadi](y.mohammadi@ucl.ac.uk) [Joe Ziminski](https://www.sainsburywellcome.org/web/people/joe-ziminski)| practical |
    | 04 | Feb 01 | [Circular statistics](https://github.com/joacorapela/neuroinformatics24/blob/master/practicals/04_circulaVariables_bootstrap) | [Joaquin Rapela](https://www.gatsby.ucl.ac.uk/~rapela) [Yousef Mohammadi](y.mohammadi@ucl.ac.uk)| practical |
    | 05 | Feb 08 | Singular Value Decomposition | [Will Dorrell](https://www.williamdorrell.co.uk/)| practical |
    | 06 | Feb 16 | [Linear Regression](https://github.com/joacorapela/neuroinformatics24/blob/master/lectures/linearRegression/swc_neuroinformatics_linreg.pdf) | [Lior Fox](https://liorfox.github.io/) | lecture |
    | 06 | Feb 17 | Linear Regression | [Lior Fox](https://liorfox.github.io/) | practical |
    | 07 | Feb 22 | [Linear Dynamical Systems(lectures/07_linearDynamicalSystems) | [Aniruddh Galgali](https://www.linkedin.com/in/anirgalgali/) [Joaquin Rapela](https://www.gatsby.ucl.ac.uk/~rapela) | lecture |
    | 07 | Feb 23 | [Linear Dynamical Systems](practicals/06_linearDynamicalSystems/README.md) | [Aniruddh Galgali](https://www.linkedin.com/in/anirgalgali/) [Joaquin Rapela](https://www.gatsby.ucl.ac.uk/~rapela) | practical |
    | 08 | Feb 29 | No class (CoSyNe) | | |
    | 09 | Mar 07 | Artificial Neural Networks | [Erin Grant](https://eringrant.github.io/) | lecture |
    | 09 | Mar 08 | Artificial Neural Networks | [Erin Grant](https://eringrant.github.io/) | practical |
    | 10 | Mar 14 | Experimental Control with Bonsai | [Goncalo Lopez](https://neurogears.org/about-us/) [Joaquin Rapela](https://www.gatsby.ucl.ac.uk/~rapela) | lecture |
    | 10 | Mar 15 | Reinforcement learning | [Jesse Gerts](https://scholar.google.com/citations?user=4xusDVAAAAAJ&hl=en) | lecture |
    | 11 | Mar 22 | Experimental Control with Bonsai | [Goncalo Lopez](https://neurogears.org/about-us/) [Joaquin Rapela](https://www.gatsby.ucl.ac.uk/~rapela) | practical |
    | 11 | Mar 23 | Reinforcement learning | [Jesse Gerts](https://scholar.google.com/citations?user=4xusDVAAAAAJ&hl=en) (unconfirmed) | practical |

- lecture notes for discussion sessions can be found [here](https://github.com/joacorapela/neuroinformatics24/tree/master/practicals)

- worksheets can be found [here](https://github.com/joacorapela/neuroinformatics24/tree/master/worksheets)

- running scripts: we recommend that you run the provided scripts in a conda environment. Before running any script do (only once):

    1. `conda create -n neuroi python`
    2. clone this repository (`git clone git@github.com:joacorapela/neuroinformatics24.git`)

    3. change to the repository directory (`cd neuroinformatics24`)
    4. activate your conda environment (`conda activate neuroi`)
    5. type `pip install -r requirements.txt`

    The you can run any script by (for example):

    - `cd practicals/02_LFPs_spectralAnalysis/exercises/`
    - `python doReconstructionExercise.py`

- If you have any problem running scripts in this repo, please contact [Joaquin Rapela](https://www.gatsby.ucl.ac.uk/~rapela).

