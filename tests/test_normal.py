import pystan


def test_normal_compile():
    """Compile a simple model."""
    program_code = 'parameters {real y;} model {y ~ normal(0,1);}'
    posterior = pystan.compile(program_code, data={})
    assert posterior is not None


def test_normal_sample():
    """Sample from normal distribution."""
    program_code = 'parameters {real y;} model {y ~ normal(0,1);}'
    posterior = pystan.compile(program_code, data={})
    assert posterior is not None
    fit = posterior.sample()
    assert fit.values.shape == (1, 1000, 1)  # 1 chain, n samples, 1 param
    df = fit.to_frame()
    assert len(df['y']) == 1000
    assert -5 < df['y'].mean() < 5


def test_normal_sample_chains():
    """Sample from normal distribution with more than one chain."""
    program_code = 'parameters {real y;} model {y ~ normal(0,1);}'
    posterior = pystan.compile(program_code, data={})
    assert posterior is not None
    fit = posterior.sample(num_chains=2)
    assert fit.values.shape == (2, 1000, 1)  # 1 chain, n samples, 1 param
    df = fit.to_frame()
    assert len(df['y']) == 2000
    assert -5 < df['y'].mean() < 5


def test_normal_sample_args():
    """Sample from normal distribution with compile arguments."""
    program_code = 'parameters {real y;} model {y ~ normal(0,1);}'
    posterior = pystan.compile(program_code, data={}, random_seed=1)
    assert posterior is not None
    fit = posterior.sample(num_samples=350, num_thin=2)
    df = fit.to_frame()
    assert len(df['y']) == 350 // 2
    assert -5 < df['y'].mean() < 5
    assert fit.to_panel().shape == (1, 350 // 2, 1)  # 1 chain, n samples, 1 parameter
    assert fit.to_panel().loc[:, :, 'y'].shape == (350 // 2, 1)
