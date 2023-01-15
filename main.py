import publisher
import subscriber
import concurrent.futures


# Final Project // IOT Course, HIT // Yael Levi & Matan Maimon & Efi Tzaig


def main():
    # Create heart rate dashboard // for specific client insert id // for all clients insert 0
    client_id = 207196205
    # Run publisher and subscriber in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        subscriber_future = executor.submit(subscriber.subscribe, client_id)
        publisher_future = executor.submit(publisher.generate_heart_rate_and_publish, client_id)
        concurrent.futures.wait([subscriber_future, publisher_future])


main()


