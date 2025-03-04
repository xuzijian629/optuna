import numpy as np
import pytest

from optuna.study import create_study
from optuna.trial import Trial
from optuna.visualization import plot_optimization_history


def test_target_is_none_and_study_is_multi_obj() -> None:

    study = create_study(directions=["minimize", "minimize"])
    with pytest.raises(ValueError):
        plot_optimization_history(study)


@pytest.mark.parametrize("direction", ["minimize", "maximize"])
def test_plot_optimization_history(direction: str) -> None:
    # Test with no trial.
    study = create_study(direction=direction)
    figure = plot_optimization_history(study)
    assert len(figure.data) == 0

    def objective(trial: Trial) -> float:

        if trial.number == 0:
            return 1.0
        elif trial.number == 1:
            return 2.0
        elif trial.number == 2:
            return 0.0
        return 0.0

    # Test with a trial.
    study = create_study(direction=direction)
    study.optimize(objective, n_trials=3)
    figure = plot_optimization_history(study)
    assert len(figure.data) == 2
    assert figure.data[0].x == (0, 1, 2)
    assert figure.data[0].y == (1.0, 2.0, 0.0)
    assert figure.data[1].x == (0, 1, 2)
    if direction == "minimize":
        assert np.array_equal(figure.data[1].y, np.array([1.0, 1.0, 0.0]))
    else:
        assert np.array_equal(figure.data[1].y, np.array([1.0, 2.0, 2.0]))
    assert figure.data[0].name == "Objective Value"
    assert figure.layout.yaxis.title.text == "Objective Value"

    # Test customized target.
    with pytest.warns(UserWarning):
        figure = plot_optimization_history(study, target=lambda t: t.number)
    assert len(figure.data) == 1
    assert np.array_equal(figure.data[0].x, np.array([0, 1, 2], dtype=float))
    assert np.array_equal(figure.data[0].y, np.array([0, 1, 2], dtype=float))

    # Test customized target name.
    figure = plot_optimization_history(study, target_name="Target Name")
    assert figure.data[0].name == "Target Name"
    assert figure.layout.yaxis.title.text == "Target Name"

    # Ignore failed trials.
    def fail_objective(_: Trial) -> float:
        raise ValueError

    study = create_study(direction=direction)
    study.optimize(fail_objective, n_trials=1, catch=(ValueError,))

    figure = plot_optimization_history(study)
    assert len(figure.data) == 0


@pytest.mark.parametrize("direction", ["minimize", "maximize"])
def test_plot_optimization_history_with_multiple_studies(direction: str) -> None:
    n_studies = 10

    # Test with no trial.
    studies = [create_study(direction=direction) for _ in range(n_studies)]
    figure = plot_optimization_history(studies)
    assert len(figure.data) == 0

    def objective(trial: Trial) -> float:

        if trial.number == 0:
            return 1.0
        elif trial.number == 1:
            return 2.0
        elif trial.number == 2:
            return 0.0
        return 0.0

    # Test with trials.
    studies = [create_study(direction=direction) for _ in range(n_studies)]
    for study in studies:
        study.optimize(objective, n_trials=3)
    figure = plot_optimization_history(studies)
    assert len(figure.data) == 2 * n_studies
    assert figure.data[0].x == (0, 1, 2)
    assert figure.data[0].y == (1.0, 2.0, 0.0)
    assert figure.data[1].x == (0, 1, 2)
    if direction == "minimize":
        assert np.array_equal(figure.data[1].y, np.array([1.0, 1.0, 0.0]))
    else:
        assert np.array_equal(figure.data[1].y, np.array([1.0, 2.0, 2.0]))
    assert figure.data[0].name == f"Objective Value of {studies[0].study_name}"
    assert figure.layout.yaxis.title.text == "Objective Value"

    # Test customized target.
    with pytest.warns(UserWarning):
        figure = plot_optimization_history(studies, target=lambda t: t.number)
    assert len(figure.data) == 1 * n_studies
    assert np.array_equal(figure.data[0].x, np.array([0, 1, 2], dtype=float))
    assert np.array_equal(figure.data[0].y, np.array([0, 1, 2], dtype=float))

    # Test customized target name.
    figure = plot_optimization_history(studies, target_name="Target Name")
    assert figure.data[0].name == f"Target Name of {studies[0].study_name}"
    assert figure.layout.yaxis.title.text == "Target Name"

    # Ignore failed trials.
    def fail_objective(_: Trial) -> float:
        raise ValueError

    studies = [create_study(direction=direction) for _ in range(n_studies)]
    for study in studies:
        study.optimize(fail_objective, n_trials=1, catch=(ValueError,))

    figure = plot_optimization_history(studies)
    assert len(figure.data) == 0


@pytest.mark.parametrize("direction", ["minimize", "maximize"])
def test_plot_optimization_history_with_error_bar(direction: str) -> None:
    n_studies = 10

    # Test with no trial.
    studies = [create_study(direction=direction) for _ in range(n_studies)]
    figure = plot_optimization_history(studies, error_bar=True)
    assert len(figure.data) == 0

    def objective(trial: Trial) -> float:

        if trial.number == 0:
            return 1.0
        elif trial.number == 1:
            return 2.0
        elif trial.number == 2:
            return 0.0
        return 0.0

    # Test with trials.
    studies = [create_study(direction=direction) for _ in range(n_studies)]
    for study in studies:
        study.optimize(objective, n_trials=3)
    figure = plot_optimization_history(studies, error_bar=True)
    assert len(figure.data) == 4
    assert np.array_equal(figure.data[0].x, (0, 1, 2))
    assert np.array_equal(figure.data[0].y, (1.0, 2.0, 0.0))
    assert np.array_equal(figure.data[1].x, (0, 1, 2))
    if direction == "minimize":
        assert np.array_equal(figure.data[1].y, np.array([1.0, 1.0, 0.0]))
    else:
        assert np.array_equal(figure.data[1].y, np.array([1.0, 2.0, 2.0]))
    assert figure.data[0].name == "Objective Value"
    assert figure.layout.yaxis.title.text == "Objective Value"

    # Test customized target.
    with pytest.warns(UserWarning):
        figure = plot_optimization_history(studies, target=lambda t: t.number, error_bar=True)
    assert len(figure.data) == 1
    assert np.array_equal(figure.data[0].x, np.array([0, 1, 2], dtype=float))
    assert np.array_equal(figure.data[0].y, np.array([0, 1, 2], dtype=float))

    # Test customized target name.
    figure = plot_optimization_history(studies, target_name="Target Name", error_bar=True)
    assert figure.data[0].name == "Target Name"
    assert figure.layout.yaxis.title.text == "Target Name"

    # Ignore failed trials.
    def fail_objective(_: Trial) -> float:
        raise ValueError

    studies = [create_study(direction=direction) for _ in range(n_studies)]
    for study in studies:
        study.optimize(fail_objective, n_trials=1, catch=(ValueError,))

    figure = plot_optimization_history(studies, error_bar=True)
    assert len(figure.data) == 0
