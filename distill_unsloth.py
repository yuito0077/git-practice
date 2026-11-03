import os
import torch
import json
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

try:
    from unsloth import FastLanguageModel, is_bfloat16_supported
except ImportError:
    # Handle environment where unsloth is not installed
    pass

def main():
    max_seq_length = 2048
    dtype = None # None for auto detection
    load_in_4bit = True # Use 4bit quantization to reduce memory usage

    # 1. Load Model (e.g., Llama-3.2-3B for distillation)
    model_name = "unsloth/Llama-3.2-3B-Instruct"
    print(f"Loading {model_name} with Unsloth...")

    try:
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name = model_name,
            max_seq_length = max_seq_length,
            dtype = dtype,
            load_in_4bit = load_in_4bit,
        )
    except NameError:
        print("Unsloth not installed. Please install it to load the model.")
        return

    # 2. Add LoRA
    print("Applying QLoRA...")
    model = FastLanguageModel.get_peft_model(
        model,
        r = 16,
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                          "gate_proj", "up_proj", "down_proj"],
        lora_alpha = 16,
        lora_dropout = 0,
        bias = "none",
        use_gradient_checkpointing = "unsloth",
        random_state = 3407,
        use_rslora = False,
        loftq_config = None,
    )

    # 3. Load Teacher-Student Distillation dataset
    dataset_path = os.environ.get("DATASET_PATH", "teacher_student_data.jsonl")
    if os.path.exists(dataset_path):
        dataset = load_dataset("json", data_files={"train": dataset_path})["train"]
    else:
        print(f"Dataset {dataset_path} not found. Creating a dummy distillation dataset.")
        dummy_data = [
            {
                "instruction": "Solve the following task using tools.",
                "input": "User: What is 2+2?",
                "output": '```json\n{"tool": "calculator", "args": {"expression": "2+2"}}\n```'
            }
        ]
        with open("teacher_student_data.jsonl", "w") as f:
            for d in dummy_data:
                f.write(json.dumps(d) + "\n")
        dataset = load_dataset("json", data_files={"train": "teacher_student_data.jsonl"})["train"]

    # Formatting function
    prompt_template = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

    EOS_TOKEN = tokenizer.eos_token
    def formatting_prompts_func(examples):
        instructions = examples["instruction"]
        inputs       = examples["input"]
        outputs      = examples["output"]
        texts = []
        for instruction, input, output in zip(instructions, inputs, outputs):
            text = prompt_template.format(instruction, input, output) + EOS_TOKEN
            texts.append(text)
        return { "text" : texts }

    dataset = dataset.map(formatting_prompts_func, batched = True)

    # 4. Train
    print("Starting training...")
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        dataset_num_proc = 2,
        packing = False,
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            max_steps = 100, # Set based on your data size
            learning_rate = 2e-4,
            fp16 = not is_bfloat16_supported(),
            bf16 = is_bfloat16_supported(),
            logging_steps = 10,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = "outputs",
            report_to = "none"
        ),
    )

    trainer_stats = trainer.train()

    # 5. Save model
    print("Saving the distilled QLoRA model...")
    model.save_pretrained("distilled_lora_model")
    tokenizer.save_pretrained("distilled_lora_model")
    print("Distillation complete.")

if __name__ == "__main__":
    main()
