import optuna
import os
import yaml
import subprocess
import shutil

# Models to merge
BASE_MODEL = "Qwen/Qwen2.5-3B-Instruct"
CODER_MODEL = "Qwen/Qwen2.5-Coder-3B"
OUTPUT_DIR = "./merged_models"

def evaluate_model(model_path):
    """
    Evaluates the merged model on autonomous agent tool-calling capabilities.
    In a real scenario, this would load the model using vLLM or HF Transformers,
    run it against a benchmark like the Berkeley Function Calling Leaderboard,
    and return the accuracy score.
    """
    print(f"Evaluating model at {model_path} for tool-calling capabilities...")
    # Mock score for pipeline demonstration purposes
    # A real implementation would compute metrics based on prompt completions
    score = 0.85
    return score

def objective(trial):
    # CMA-ES will sample these parameters
    density = trial.suggest_float("density", 0.1, 0.9)
    weight = trial.suggest_float("weight", 0.1, 0.9)

    trial_dir = os.path.join(OUTPUT_DIR, f"trial_{trial.number}")
    os.makedirs(trial_dir, exist_ok=True)

    # Create DARE-TIES configuration
    config = {
        "models": [
            {
                "model": BASE_MODEL,
                # Base model doesn't need density/weight
            },
            {
                "model": CODER_MODEL,
                "parameters": {
                    "density": density,
                    "weight": weight
                }
            }
        ],
        "merge_method": "dare_ties",
        "base_model": BASE_MODEL,
        "parameters": {
            "int8_mask": True
        },
        "dtype": "bfloat16"
    }

    config_path = os.path.join(trial_dir, "merge_config.yml")
    with open(config_path, "w") as f:
        yaml.dump(config, f)

    merge_output_path = os.path.join(trial_dir, "merged")

    print(f"Starting merge for trial {trial.number} with density={density:.2f}, weight={weight:.2f}")

    # Run mergekit via shell subprocess
    try:
        # Note: --cuda removed for compatibility if no GPU is present in test environment.
        # Add --cuda for real execution on a GPU instance.
        subprocess.run([
            "mergekit-yaml", config_path, merge_output_path,
            "--lazy-unpickle",
            "--allow-crimes"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Merge failed for trial {trial.number}: {e}")
        # Prune the trial if the merge fails (e.g. out of memory)
        raise optuna.exceptions.TrialPruned()
    except FileNotFoundError:
        print("mergekit-yaml not found. Is it installed? Skipping actual merge for demonstration.")
        # If mergekit is not installed, we can simulate the merge for pipeline testing
        os.makedirs(merge_output_path, exist_ok=True)
        with open(os.path.join(merge_output_path, "config.json"), "w") as f:
            f.write('{"model_type": "qwen2"}')

    # Evaluate the merged model
    score = evaluate_model(merge_output_path)

    # To save disk space during evolution, we can delete the model if we wanted,
    # but we'll keep it to export the best one later.

    return score

def convert_to_gguf(model_path, output_gguf_path):
    print(f"Converting {model_path} to GGUF format...")
    llama_cpp_path = "./llama.cpp"
    if not os.path.exists(llama_cpp_path):
        print("llama.cpp not found in current directory. Skipping GGUF conversion.")
        return

    convert_script = os.path.join(llama_cpp_path, "convert_hf_to_gguf.py")

    if not os.path.exists(convert_script):
        # Fallback to older naming if needed
        convert_script = os.path.join(llama_cpp_path, "convert.py")

    if not os.path.exists(convert_script):
        print("GGUF conversion script not found in llama.cpp directory.")
        return

    try:
        subprocess.run([
            "python3", convert_script, model_path,
            "--outfile", output_gguf_path,
            "--outtype", "q8_0" # Quantize to 8-bit for Ollama
        ], check=True)
        print(f"Successfully created GGUF model at {output_gguf_path}")
    except subprocess.CalledProcessError as e:
        print(f"GGUF conversion failed: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Use Optuna's CMA-ES Sampler
    sampler = optuna.samplers.CmaEsSampler()
    study = optuna.create_study(direction="maximize", sampler=sampler, study_name="qwen_evolve_merge")

    # Optimize over 5 trials for demonstration. In practice, this would be 50-100+
    study.optimize(objective, n_trials=5)

    print("\nOptimization finished.")
    print("Best trial:")
    trial = study.best_trial

    print(f"  Value (Score): {trial.value}")
    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")

    # Paths for best model
    best_model_path = os.path.join(OUTPUT_DIR, f"trial_{trial.number}", "merged")
    best_gguf_path = os.path.join(OUTPUT_DIR, "best_model_q8_0.gguf")

    # Export best model to GGUF for local Ollama deployment
    if os.path.exists(best_model_path):
        convert_to_gguf(best_model_path, best_gguf_path)
    else:
        print("Best model directory not found. Did the merge succeed?")

if __name__ == "__main__":
    main()
