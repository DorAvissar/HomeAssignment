import multiprocessing
import time

def cpu_stress_test():
    while True:
        pass

if __name__ =='__main__':
    # Number of CPU cores to stress (e.g., all available cores)
    num_cores = multiprocessing.cpu_count()

    processes = []
    for _ in range(num_cores):
        p = multiprocessing.Process(target=cpu_stress_test)
        p.start()
        processes.append(p)

    # Run the stress test for a specified duration (e.g., 60 seconds)
    stress_duration = 60  # seconds
    time.sleep(stress_duration)

    # Terminate all processes
    for p in processes:
        p.terminate()
        p.join()