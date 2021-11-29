"""
Judger server service main
"""
import json
import sys
import pika
from service import judge
from service.errors import CompileError
from language import config


def callback(channel, method, properties, body):
    """
    Callback function for receiving message
    """
    body = json.loads(body)
    language_config = config.LanguageConfig(
        body["language"], body["max_cpu_time"], body["max_memory"]
    ).config
    try:
        result = judge.judge(
            language_config, body["source_code"], body["max_cpu_time"], body["max_memory"],
            str(body["submission_id"]), str(body["test_case_id"]), body["program_name"]
        )
        print({
            "submission_id": body["submission_id"],
            "compile_error": 0,
            "results": result
        })
    except CompileError as _:
        print({
            "submission_id": body["submission_id"],
            "compile_error": 1,
            "results": []
        })
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    """
    Main function
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('10.211.55.23'))
    channel = connection.channel()
    queue_name = "program_submission"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            print('Interrupted')
            sys.exit(0)
        except SystemExit:
            print('Interrupted')
            raise
