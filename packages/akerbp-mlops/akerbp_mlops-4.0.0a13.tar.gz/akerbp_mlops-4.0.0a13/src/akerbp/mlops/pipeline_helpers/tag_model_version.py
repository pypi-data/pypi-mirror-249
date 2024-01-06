import argparse
import logging
import os
import subprocess
from pathlib import Path

import akerbp.mlops.model_manager as mm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--model_name",
        type=str,
        help="Name of model. If not provided, it will be inferred from the mlops_settings.yaml file.",
        default="",
        required=False,
    )
    args = parser.parse_args()
    model_name = args.model_name
    if not model_name:
        from akerbp.mlops.core.config import read_project_settings

        # resorting to first model name in settings
        model_name = read_project_settings()[0].model_name

    logging.disable()
    mm.setup()
    env = os.environ.get("MODEL_ENV")
    try:
        latest_deployed_model = (
            mm.get_model_version_overview(
                model_name=model_name,
                env=env,
                output_logs=False,
            )
            .sort_values(by="uploaded_time", ascending=False)
            .iloc[0]
        )
        version_number = latest_deployed_model.external_id.split("/")[-1]

        try:
            bash_script_path = Path(__file__).resolve().parent / "tag_commit.sh"
            subprocess.run(["chmod", "+x", bash_script_path])
            subprocess.run([bash_script_path, version_number])
        except subprocess.CalledProcessError as e:
            print(f"Tagging commit returned an error: {e}")
    except IndexError as e:
        raise Exception(
            f"No version of model {model_name} found in the model registry"
        ) from e


if __name__ == "__main__":
    main()  # type: ignore
