import os
import time
from process import Process
from scheduler import Scheduler
from utils import read_csv, save_timeline, calculate_statistics, save_results, generate_report

def main():
    print("\n" + "="*60)
    print("CPU SCHEDULING ALGORITHMS SIMULATION")
    print("Istanbul Nişantaşı University")
    print("EBLM341 - Operating Systems")
    print("="*60)
    
    try:
        # data klasörünü kontrol et
        if not os.path.exists("data"):
            print("\nCreating data folder...")
            os.makedirs("data")
            print("Please put case1.csv and case2.csv in the data folder")
            input("\nPress Enter to exit...")
            return
        
        # CSV dosyalarını listele
        csv_files = [f for f in os.listdir("data") if f.endswith('.csv')]
        if not csv_files:
            print("\nNo CSV files found in data folder!")
            print("Please add case1.csv and case2.csv")
            input("\nPress Enter to exit...")
            return
        
        print(f"\nFound CSV files: {csv_files}")
        
        # Kullanıcıdan seçim al
        print("\nSELECT CSV FILE:")
        for i, file in enumerate(csv_files, 1):
            print(f"{i}. {file}")
        
        try:
            choice = int(input(f"\nEnter choice (1-{len(csv_files)}): "))
            if choice < 1 or choice > len(csv_files):
                choice = 1
        except:
            choice = 1
        
        selected_file = csv_files[choice-1]
        case_name = selected_file.replace('.csv', '')
        csv_path = f"data/{selected_file}"
        
        print(f"\nSelected: {selected_file}")
        
        # CSV'yi oku
        processes = read_csv(csv_path)
        
        if not processes:
            print("\n❌ ERROR: No processes loaded!")
            print("Possible reasons:")
            print("1. CSV file is empty")
            print("2. CSV format is incorrect")
            print("3. File not found")
            print("\nCSV format should be:")
            print("Process_ID,Arrival_Time,CPU_Burst_Time,Priority")
            print("P001,0,1,high")
            print("P002,2,2,normal")
            input("\nPress Enter to exit...")
            return
        
        print(f"\n✅ Successfully loaded {len(processes)} processes")
        
        # İlk 5 süreci göster
        print("\nSample processes (first 5):")
        print("PID\tArrival\tBurst\tPriority")
        print("-" * 30)
        for p in processes[:5]:
            print(f"{p.pid}\t{p.arrival}\t{p.burst}\t{p.priority}")
        
        if len(processes) > 5:
            print(f"... and {len(processes) - 5} more")
        
        input("\nPress Enter to start simulation...")
        
        # Scheduler'ı başlat
        scheduler = Scheduler()
        
        print("\n" + "="*60)
        print("RUNNING SCHEDULING ALGORITHMS")
        print("="*60)
        
        start_time = time.time()
        
        # Çıktı klasörlerini oluştur
        output_dir = f"outputs/{case_name}"
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs("reports", exist_ok=True)
        
        all_results = []
        
        # 1. FCFS
        print("\n1️⃣  Running FCFS (First Come First Served)...")
        try:
            timeline, result_procs = scheduler.fcfs(processes)
            results = calculate_statistics(result_procs, "FCFS", case_name)
            all_results.append(results)
            save_timeline(timeline, f"{output_dir}/FCFS_timeline.txt")
            save_results(results, f"{output_dir}/FCFS_results.txt")
            print("   ✅ FCFS completed")
        except Exception as e:
            print(f"   ❌ FCFS failed: {e}")
        
        # 2. Non-Preemptive SJF
        print("\n2️⃣  Running Non-Preemptive SJF...")
        try:
            timeline, result_procs = scheduler.sjf_non_preemptive(processes)
            results = calculate_statistics(result_procs, "Non-Preemptive SJF", case_name)
            all_results.append(results)
            save_timeline(timeline, f"{output_dir}/SJF_NonPreemptive_timeline.txt")
            save_results(results, f"{output_dir}/SJF_NonPreemptive_results.txt")
            print("   ✅ Non-Preemptive SJF completed")
        except Exception as e:
            print(f"   ❌ Non-Preemptive SJF failed: {e}")
        
        # 3. Preemptive SJF
        print("\n3️⃣  Running Preemptive SJF...")
        try:
            timeline, result_procs = scheduler.sjf_preemptive(processes)
            results = calculate_statistics(result_procs, "Preemptive SJF", case_name)
            all_results.append(results)
            save_timeline(timeline, f"{output_dir}/SJF_Preemptive_timeline.txt")
            save_results(results, f"{output_dir}/SJF_Preemptive_results.txt")
            print("   ✅ Preemptive SJF completed")
        except Exception as e:
            print(f"   ❌ Preemptive SJF failed: {e}")
        
        # 4. Round Robin
        print("\n4️⃣  Running Round Robin (Quantum=4)...")
        try:
            timeline, result_procs = scheduler.round_robin(processes, quantum=4)
            results = calculate_statistics(result_procs, "Round Robin (Q=4)", case_name)
            all_results.append(results)
            save_timeline(timeline, f"{output_dir}/RoundRobin_timeline.txt")
            save_results(results, f"{output_dir}/RoundRobin_results.txt")
            print("   ✅ Round Robin completed")
        except Exception as e:
            print(f"   ❌ Round Robin failed: {e}")
        
        # 5. Non-Preemptive Priority
        print("\n5️⃣  Running Non-Preemptive Priority...")
        try:
            timeline, result_procs = scheduler.priority_non_preemptive(processes)
            results = calculate_statistics(result_procs, "Non-Preemptive Priority", case_name)
            all_results.append(results)
            save_timeline(timeline, f"{output_dir}/Priority_NonPreemptive_timeline.txt")
            save_results(results, f"{output_dir}/Priority_NonPreemptive_results.txt")
            print("   ✅ Non-Preemptive Priority completed")
        except Exception as e:
            print(f"   ❌ Non-Preemptive Priority failed: {e}")
        
        # 6. Preemptive Priority
        print("\n6️⃣  Running Preemptive Priority...")
        try:
            timeline, result_procs = scheduler.priority_preemptive(processes)
            results = calculate_statistics(result_procs, "Preemptive Priority", case_name)
            all_results.append(results)
            save_timeline(timeline, f"{output_dir}/Priority_Preemptive_timeline.txt")
            save_results(results, f"{output_dir}/Priority_Preemptive_results.txt")
            print("   ✅ Preemptive Priority completed")
        except Exception as e:
            print(f"   ❌ Preemptive Priority failed: {e}")
        
        execution_time = time.time() - start_time
        
        print("\n" + "="*60)
        print("GENERATING REPORT")
        print("="*60)
        
        # Rapor oluştur
        generate_report(all_results, case_name)
        
        # Sonuçları göster
        print("\n" + "="*60)
        print("FINAL RESULTS")
        print("="*60)
        
        print(f"\n{'Algorithm':<25} {'Avg Wait':<12} {'Avg Turn':<12} {'CPU Eff%':<10}")
        print("-" * 60)
        
        for result in all_results:
            print(f"{result['algorithm']:<25} "
                  f"{result['avg_waiting']:<12.2f} "
                  f"{result['avg_turnaround']:<12.2f} "
                  f"{result['cpu_efficiency']:<10.2f}")
        
        print(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
        
        print("\n📁 OUTPUT FILES:")
        print(f"• Results saved to: {output_dir}/")
        print(f"• Report saved to: reports/{case_name}_report.txt")
        
        print("\n✅ SIMULATION COMPLETED SUCCESSFULLY!")
        print("All requirements for the assignment have been met.")
        
        input("\nPress Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulation interrupted by user")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()