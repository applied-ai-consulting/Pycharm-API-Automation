#!/bin/bash

# Activate venv if not activated yet
#if [[ "$VIRTUAL_ENV" == "" ]]
#then
  #source chmod +x ./venv/bin/activate
#fi

DEFAULT_SCENARIO_SET_FILE="scenario_set.yaml"
SCENARIO_SET_FILE=$DEFAULT_SCENARIO_SET_FILE
# Params
while test $# -gt 0; do
  case "$1" in
    -h|--help)
      echo "usage: pytest.sh"
      echo " "
      echo "general:"
      echo "  -h, --help		show help message for pytest.sh followed by help message for pytest."
      echo "  --scenario-set-file=SCENARIO_SET_FILE"
      echo "			Test scenario file in YAML format which must be located under configs/ directory."
      echo "			The file name must have the prefix 'scenario_set_' and file extension '.yaml'."
      echo " "
      echo "pytest options:"
      echo "  [options] [file_or_dir] [file_or_dir] [...]"
      echo "			pytest options. "
      echo " "

      pytest -h
      exit 0
      ;;
    --scenario-set-file=*)
      SCENARIO_SET_FILE="${1#*=}"
      if [ "$SCENARIO_SET_FILE" == "" ]; then
        echo "No scenario set file is specified. Please specify one."
        exit 1
      fi
      shift
      ;;
    --scenario-set-file)
      echo "No scenario set file is specified. Please specify one."
      exit 1
      ;;
    *)
      break
      ;;
  esac
done

if [ "$SCENARIO_SET_FILE" != "$DEFAULT_SCENARIO_SET_FILE" ]; then
    echo "Copying $SCENARIO_SET_FILE to $DEFAULT_SCENARIO_SET_FILE"
    cp ./configs/$SCENARIO_SET_FILE ./configs/$DEFAULT_SCENARIO_SET_FILE
fi

pytest $@
