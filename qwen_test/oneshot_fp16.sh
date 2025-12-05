PREFIX=/home/skymizer/20250916/ecosystem-umbrella/prefix
LOADABLE="/home/skymizer/20250916/ecosystem-umbrella/demo-qwen-inst/qwen2_5-1_5b_inst_dmaosr_bypass.emf"
VOCAB="/home/skymizer/20250916/ecosystem-umbrella/demo-qwen-inst/qwen-vocab.gguf"

if [ -z "$1" ]; then
  echo "Usage: $0 '<prompt>'"
  exit 1
fi
LD_LIBRARY_PATH=${PREFIX}/lib \
GGML_XTHOUGHT_LOADABLE_PATH="${LOADABLE}" \
GGML_XTHOUGHT_MODEL_CARD="llama2-et2rt-et2" \
${PREFIX}/bin/llama-cli -m ${VOCAB} \
  --jinja \
  --temp 0 \
  --no-warmup \
  --n-predict 512 \
  --no-conversation \
  --no-display-prompt \
  --repeat-penalty 1.05 \
  -p "$1" \
  2> stderr.log
  # when --no_conversation mode is applied, system prompt is ignored
  #   --system-prompt "Answer simple questions within 200 tokens and follow-up questions within 800 tokens." \
    # --verbose-prompt \
    # --chat-template chatml \
    # -no-cnv \
#   2> stderr.log
#   --repeat-penalty 1.05 \
