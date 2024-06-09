. .\.venv\Scripts\Activate.ps1

# VGA,  4:3,    640,    480,    0.307, 0.3M
# SVGA, 4:3,    800,    600,    0.480, 0.5M
# XGA,  4:3,    1024,   768,    0.786, 0.8M
# WXGA, 16:9,   1280,   720,    0.922, 0.9M
# HD,   16:9,   1600,   900,    1.440, 1.4M
# UXGA, 4:3,    1600,   1200,   1.920, 1.9M
# FHD,  16:9,   1920,   1080,   2.074, 2.1M
# QWXGA,16:9,   2048,   1152,   2.359, 2.4M
# QXGA, 4:3,    2048,   1536,   3.145, 3.1M
# QHD,  16:9,   2560,   1440,   3.686, 3.7M
# UHD,  16:9,   3840,   2160,   8.294, 8.3M

# HD,   16:9,   1600,   900,    1.440, 1.4M
# FHD,  16:9,   1920,   1080,   2.074, 2.1M
# QHD,  16:9,   2560,   1440,   3.686, 3.7M
# UHD,  16:9,   3840,   2160,   8.294, 8.3M

$dt_str = Get-Date -UFormat "%Y%m%d_%H%M%S"
$OUTPUT_DIR = "--output_dir=.output/" + $dt_str

$ITERATIONS = "--iterations=100"
$USE_CPU = "--device=cpu"
$USE_GPU = "--device=cuda"
$IMG_SIZE_1600X0900  = @("--image_width=1600", "--image_height=900")
$IMG_SIZE_1920x1080 = @("--image_width=1920", "--image_height=1080")
$IMG_SIZE_2560x1440 = @("--image_width=2560", "--image_height=1440")
$IMG_SIZE_3840x2160 = @("--image_width=3840", "--image_height=2160")

# GPU
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_1600X0900 --model_type="vit_b"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_1600X0900 --model_type="vit_l"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_1600X0900 --model_type="vit_h"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_1920x1080 --model_type="vit_b"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_1920x1080 --model_type="vit_l"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_1920x1080 --model_type="vit_h"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_2560x1440 --model_type="vit_b"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_2560x1440 --model_type="vit_l"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_2560x1440 --model_type="vit_h"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_3840x2160 --model_type="vit_b"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_3840x2160 --model_type="vit_l"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_GPU $IMG_SIZE_3840x2160 --model_type="vit_h"

# CPU
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_1600X0900 --model_type="vit_b"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_1600X0900 --model_type="vit_l"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_1600X0900 --model_type="vit_h"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_1920x1080 --model_type="vit_b"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_1920x1080 --model_type="vit_l"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_1920x1080 --model_type="vit_h"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_2560x1440 --model_type="vit_b"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_2560x1440 --model_type="vit_l"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_2560x1440 --model_type="vit_h"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_3840x2160 --model_type="vit_b"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_3840x2160 --model_type="vit_l"
python .\measure_time_sam.py --multimask_output $OUTPUT_DIR $ITERATIONS $USE_CPU $IMG_SIZE_3840x2160 --model_type="vit_h"
