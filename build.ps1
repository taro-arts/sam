python -m venv .venv
. .\.venv\Scripts\Activate.ps1

python -m pip install -U pip
python -m pip install -r requirements.txt
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

git clone https://github.com/facebookresearch/segment-anything.git
python -m pip install -e ./segment-anything