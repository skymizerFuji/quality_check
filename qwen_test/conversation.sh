PREFIX=/home/skymizer/20250916/ecosystem-umbrella/prefix

LOADABLE="/home/skymizer/20250916/ecosystem-umbrella/demo-qwen-inst/qwen2_5-1_5b_inst_dmaosr.emf"
VOCAB="/home/skymizer/20250916/ecosystem-umbrella/demo-qwen-inst/qwen-vocab.gguf"

LD_LIBRARY_PATH=${PREFIX}/lib \
GGML_XTHOUGHT_LOADABLE_PATH="${LOADABLE}" \
GGML_XTHOUGHT_MODEL_CARD="llama2-et2rt-et2" \
${PREFIX}/bin/llama-cli -m ${VOCAB} --conversation \
  --jinja \
  --system-prompt "You are a helpful assistant. When answering, unless requested otherwise, give the answer directly without explaining your thought process." \
  --interactive-first \
  --temp 0 \
  --no-warmup \
  --repeat-penalty 1.05 \
  --n-predict 512 \
  2> stderr.log

  # --ctx-size 96
#   --verbose-prompt
#  2> /dev/null
  #2>&1 | tee /tmp/qwen.log
  #--chat-template deepseek \