import argparse
import gradio as gr
from src.Systems.BrocaSystems import BrocaSystems

from MindMap.LogManager import LogManager

logManager = LogManager()
def main(host, port, stream):
    chatbot = BrocaSystems(logManager=logManager)

    with gr.Blocks() as demo:
        gr.Markdown("# Streaming Chatbot")

        chatbot_ui = gr.Chatbot()
        with gr.Row():
            with gr.Column():
                user_input = gr.Textbox(show_label=False, placeholder="메시지를 입력하세요")

            with gr.Column():
                send_button = gr.Button("보내기")

        def stream_user_interaction(user_input, history):
            bot_response = ""
            history.append((user_input, bot_response))

            for ai_message in chatbot.stream_chat(user_input):
                try:
                    bot_response += ai_message
                except Exception as e:
                    logManager.log_error(f"(app.py) stream_user_interaction: {e}")
                history[-1] = (user_input, ai_message)
                yield history, ""

            history[-1] = (user_input, bot_response)

        def user_interaction(user_input, history):
            ai_response = chatbot.chat(user_input)
            history = history + [(user_input, ai_response)]
            logManager.log_info(f"Model: {ai_response}")

            return history, user_input

        if stream:
            send_button.click(stream_user_interaction, inputs=[user_input, chatbot_ui], outputs=[chatbot_ui, user_input])
            user_input.submit(stream_user_interaction, inputs=[user_input, chatbot_ui], outputs=[chatbot_ui, user_input])

        else:
            send_button.click(user_interaction, inputs=[user_input, chatbot_ui], outputs=[chatbot_ui, user_input])
            user_input.submit(user_interaction, inputs=[user_input, chatbot_ui], outputs=[chatbot_ui, user_input])

    demo.launch(server_name=host, server_port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--stream", action="store_true", help="Enable streaming mode (default: False)")

    args = parser.parse_args()

    logManager.log_info(f"host  : {args.host}")
    logManager.log_info(f"port  : {args.port}")
    logManager.log_info(f"stream: {args.stream}")

    main(host=args.host, port=args.port, stream=args.stream)