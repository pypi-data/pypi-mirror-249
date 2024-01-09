import json
import subprocess
import argparse
import os

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def run_inference(inference_script):
    subprocess.run(["python", inference_script])

def train_model(training_script, pipeline_config_path, model_dir):
    subprocess.run(["python", training_script,
                    "--pipeline_config_path", pipeline_config_path,
                    "--model_dir", model_dir,
                    "--alsologtostderr"])

def evaluate_model(evaluation_script, pipeline_config_path, model_dir, checkpoint_dir):
    subprocess.run(["python", evaluation_script,
                    "--pipeline_config_path", pipeline_config_path,
                    "--model_dir", model_dir,
                    "--checkpoint_dir", checkpoint_dir,
                    "--alsologtostderr"])

def export_model(export_script, pipeline_config_path, model_dir, output_directory):
    subprocess.run(["python", export_script,
                    "--input_type", "image_tensor",
                    "--pipeline_config_path", pipeline_config_path,
                    "--trained_checkpoint_dir", model_dir,
                    "--output_directory", output_directory])

def main():
    # Load config file
    config = load_config('usv_config.json')

    # Parse Arguments
    parser = argparse.ArgumentParser(description="USV Detection Using TensorFlow Object Detection")
    parser.add_argument("--action", choices=['inference', 'train', 'evaluate', 'export'], required=True, help="Action to perform")
    args = parser.parse_args()

    # Run tasks based on provided arguments
    if args.action == 'inference':
        run_inference(config['inference_script'])
    elif args.action == 'train':
        train_model(config['training_script'], config['pipeline_config_path'], config['model_dir'])
    elif args.action == 'evaluate':
        evaluate_model(config['evaluation_script'], config['pipeline_config_path'], config['model_dir'], config['checkpoint_dir'])
    elif args.action == 'export':
        export_model(config['export_script'], config['pipeline_config_path'], config['model_dir'], config['output_directory'])

if __name__ == "__main__":
    main()

