import optuna
import kevin_toolbox.nested_dict_list as ndl
from kevin_toolbox.patches.for_optuna.serialize import for_trial
from kevin_toolbox.env_info import version


def __converter(_, v):
    if isinstance(v, optuna.storages.BaseStorage):
        return dict(name=f'optuna.storages.{v.__class__.__name__}', url=getattr(v, "url", None))
    elif isinstance(v, optuna.samplers.BaseSampler):
        return dict(name=f'optuna.samplers.{v.__class__.__name__}')
    elif isinstance(v, optuna.pruners.BasePruner):
        return dict(name=f'optuna.pruners.{v.__class__.__name__}')
    elif isinstance(v, optuna.study.StudyDirection):
        return dict(name=f'optuna.study.StudyDirection', value=v.value, description=v.name)
    elif isinstance(v, optuna.trial.BaseTrial):
        return for_trial.dump(trial=v)
    return v


def dump(study: optuna.study.Study):
    # 主要属性
    keys = ['best_params', 'best_trial', 'best_trials', 'best_value', 'direction', 'directions', 'trials', 'user_attrs']
    if version.compare(optuna.__version__, "<", "3.1.0"):
        keys.append('system_attrs')
    res_s = {k: getattr(study, k, None) for k in keys}

    # 其他信息
    res_s["__dict__"] = dict()
    for k, v in study.__dict__.items():
        if k.startswith("_"):
            k = k[1:]
        if k in ["thread_local", "optimize_lock"]:
            continue
        res_s["__dict__"][k] = v

    # 序列化
    res_s = ndl.traverse(var=res_s, match_cond=lambda _, __, v: not isinstance(v, (list, dict,)),
                         action_mode="replace", converter=__converter, b_use_name_as_idx=False,
                         b_traverse_matched_element=False)

    return res_s
