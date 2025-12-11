import csv
import os

def read_csv(filename):
    processes = []
    print(f"Reading CSV file: {filename}")
    
    try:
        # Dosyayı satır satır oku
        with open(filename, 'r') as file:
            lines = file.readlines()
            
        print(f"Total lines in file: {len(lines)}")
        
        # İlk satır başlık mı kontrol et
        first_line = lines[0].strip()
        print(f"First line: '{first_line}'")
        
        # Başlık satırını atla
        start_index = 0
        if "Process_ID" in first_line or "process_id" in first_line.lower():
            start_index = 1
            print("Header detected, skipping first line")
        
        # Her satırı işle
        for i in range(start_index, len(lines)):
            line = lines[i].strip()
            if not line:  # Boş satırları atla
                continue
                
            # Virgülle ayır
            parts = line.split(',')
            if len(parts) >= 4:
                pid = parts[0].strip()
                
                try:
                    arrival = int(parts[1].strip())
                    burst = int(parts[2].strip())
                    priority = parts[3].strip().lower()
                    
                    # Priority kontrolü
                    if priority not in ['high', 'normal', 'low']:
                        priority = 'normal'
                    
                    from process import Process
                    process = Process(pid, arrival, burst, priority)
                    processes.append(process)
                    
                except ValueError as e:
                    print(f"Error parsing line {i+1}: {line}")
                    print(f"Error: {e}")
                    continue
        
        print(f"Successfully loaded {len(processes)} processes")
        
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found!")
        print("Make sure the file exists in the data folder")
    except Exception as e:
        print(f"ERROR reading CSV: {str(e)}")
    
    return processes

def save_timeline(timeline, filename):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            for line in timeline:
                f.write(line + "\n")
        print(f"Timeline saved: {filename}")
    except Exception as e:
        print(f"Error saving timeline: {e}")

def calculate_statistics(processes, algo_name, case_name):
    if not processes:
        print("No processes to calculate statistics")
        return {}
    
    print(f"Calculating statistics for {algo_name}...")
    
    # Her süreç için zamanları hesapla
    for p in processes:
        p.calculate_times()
    
    # Bekleme süreleri
    waiting_times = [p.waiting for p in processes]
    avg_waiting = sum(waiting_times) / len(waiting_times)
    max_waiting = max(waiting_times)
    
    # Turnaround süreleri
    turnaround_times = [p.turnaround for p in processes]
    avg_turnaround = sum(turnaround_times) / len(turnaround_times)
    max_turnaround = max(turnaround_times)
    
    # Throughput (T=50,100,150,200 için)
    throughput = {}
    time_points = [50, 100, 150, 200]
    for t in time_points:
        completed = sum(1 for p in processes if p.completion <= t)
        throughput[t] = completed
    
    # CPU Verimliliği
    total_burst = sum(p.burst for p in processes)
    total_time = max(p.completion for p in processes)
    cpu_efficiency = (total_burst / total_time) * 100 if total_time > 0 else 0
    
    # Bağlam değiştirme sayısı (basit hesaplama)
    context_switches = len(processes) - 1
    
    results = {
        'algorithm': algo_name,
        'case': case_name,
        'avg_waiting': round(avg_waiting, 2),
        'max_waiting': max_waiting,
        'avg_turnaround': round(avg_turnaround, 2),
        'max_turnaround': max_turnaround,
        'throughput': throughput,
        'cpu_efficiency': round(cpu_efficiency, 2),
        'context_switches': context_switches,
        'processes': processes
    }
    
    print(f"Statistics calculated for {len(processes)} processes")
    return results

def save_results(results, filename):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            f.write(f"=== {results['algorithm']} RESULTS ===\n")
            f.write(f"Case: {results['case']}\n")
            f.write(f"Number of processes: {len(results['processes'])}\n\n")
            
            f.write("a) Waiting Times:\n")
            f.write("-----------------\n")
            f.write(f"Average Waiting Time: {results['avg_waiting']}\n")
            f.write(f"Maximum Waiting Time: {results['max_waiting']}\n\n")
            
            f.write("b) Turnaround Times:\n")
            f.write("--------------------\n")
            f.write(f"Average Turnaround Time: {results['avg_turnaround']}\n")
            f.write(f"Maximum Turnaround Time: {results['max_turnaround']}\n\n")
            
            f.write("c) Throughput:\n")
            f.write("--------------\n")
            for t, count in results['throughput'].items():
                f.write(f"T={t}: {count} processes completed\n")
            f.write("\n")
            
            f.write("d) CPU Efficiency:\n")
            f.write("------------------\n")
            f.write(f"CPU Efficiency: {results['cpu_efficiency']}%\n\n")
            
            f.write("e) Context Switches:\n")
            f.write("--------------------\n")
            f.write(f"Total Context Switches: {results['context_switches']}\n\n")
            
            # İlk 10 süreci göster
            f.write("Sample Process Details (first 10):\n")
            f.write("===================================\n")
            f.write("PID\tArrival\tBurst\tPriority\tStart\tFinish\tWaiting\tTurnaround\n")
            f.write("-" * 80 + "\n")
            
            sorted_procs = sorted(results['processes'], key=lambda x: x.pid)
            for p in sorted_procs[:10]:
                f.write(f"{p.pid}\t{p.arrival}\t{p.burst}\t{p.priority}\t"
                       f"{p.start_time}\t{p.completion}\t{p.waiting}\t{p.turnaround}\n")
            
            if len(sorted_procs) > 10:
                f.write(f"\n... and {len(sorted_procs) - 10} more processes\n")
        
        print(f"Results saved: {filename}")
        
    except Exception as e:
        print(f"Error saving results: {e}")

def generate_report(all_results, case_name):
    try:
        os.makedirs("reports", exist_ok=True)
        report_file = f"reports/{case_name}_report.txt"
        
        with open(report_file, 'w') as f:
            f.write(f"=== CPU SCHEDULING ALGORITHMS REPORT ===\n")
            f.write(f"Case: {case_name}\n")
            f.write(f"Generated on: 2024\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("PERFORMANCE COMPARISON:\n")
            f.write("=" * 100 + "\n")
            f.write(f"{'Algorithm':<25} {'Avg Wait':<12} {'Avg Turn':<12} "
                   f"{'CPU Eff%':<10} {'Throughput@200':<15}\n")
            f.write("-" * 100 + "\n")
            
            for result in all_results:
                throughput_200 = result['throughput'].get(200, 0)
                f.write(f"{result['algorithm']:<25} "
                       f"{result['avg_waiting']:<12.2f} "
                       f"{result['avg_turnaround']:<12.2f} "
                       f"{result['cpu_efficiency']:<10.2f} "
                       f"{throughput_200:<15}\n")
            
            f.write("\n\nANALYSIS:\n")
            f.write("=" * 50 + "\n")
            
            if all_results:
                # En iyi performans gösterenleri bul
                best_waiting = min(all_results, key=lambda x: x['avg_waiting'])
                best_turnaround = min(all_results, key=lambda x: x['avg_turnaround'])
                best_efficiency = max(all_results, key=lambda x: x['cpu_efficiency'])
                
                f.write("Best Performers:\n")
                f.write(f"• Best Average Waiting Time: {best_waiting['algorithm']} "
                       f"({best_waiting['avg_waiting']:.2f} time units)\n")
                f.write(f"• Best Average Turnaround Time: {best_turnaround['algorithm']} "
                       f"({best_turnaround['avg_turnaround']:.2f} time units)\n")
                f.write(f"• Highest CPU Efficiency: {best_efficiency['algorithm']} "
                       f"({best_efficiency['cpu_efficiency']:.2f}%)\n\n")
                
                f.write("Conclusion:\n")
                f.write("• FCFS is simple but has higher waiting times\n")
                f.write("• SJF algorithms provide better response times\n")
                f.write("• Round Robin ensures fairness\n")
                f.write("• Priority scheduling is useful for real-time systems\n")
        
        print(f"Report generated: {report_file}")
        
    except Exception as e:
        print(f"Error generating report: {e}")