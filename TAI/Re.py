"""
Reynolds Number Compilation Script
This script compiles all Reynolds numbers from the paper figures across LBO and TAI folders.

References:
- TAI/Time_series_figure_8.py
- TAI/Autocorrelation_Limit_cycle_figure_12.py
- TAI/Cumulative_Energy_Distribution.py
- TAI/Limit_cycle_Oscillation_Figure_13.py
"""

# ============================================================================
# TAI Reynolds Numbers (from various figures)
# ============================================================================

print("=" * 70)
print("REYNOLDS NUMBERS COMPILATION")
print("=" * 70)

# From Time_series_figure_8.py
print("\n[TAI Time Series - Figure 8]")
re_time_series = {15: 1565.85, 40: 4175.60, 53: 5532.67}
for file_num, re_val in re_time_series.items():
    print(f"  File {file_num}: Re = {re_val:.2f}")

# From Autocorrelation_Limit_cycle_figure_12.py
print("\n[TAI Autocorrelation - Figure 12]")
re_autocorr = {15: 1565.85, 40: 4175.60, 53: 5532.67}
for file_num, re_val in re_autocorr.items():
    print(f"  File {file_num}: Re = {re_val:.2f}")

# From Cumulative_Energy_Distribution.py
print("\n[TAI Cumulative Energy Distribution]")
re_cum_energy = {15: 1565.85, 45: 4697.55, 53: 5532.67}
for file_num, re_val in re_cum_energy.items():
    print(f"  File {file_num}: Re = {re_val:.2f}")

# From Limit_cycle_Oscillation_Figure_13.py
print("\n[TAI Limit Cycle Oscillation - Figure 13]")
re_limit_cycle = {15: 1565.85, 35: 3653.65, 53: 5532.67}
for file_num, re_val in re_limit_cycle.items():
    print(f"  File {file_num}: Re = {re_val:.2f}")

# ============================================================================
# Summary: Unique Reynolds Numbers
# ============================================================================

print("\n" + "=" * 70)
print("UNIQUE REYNOLDS NUMBERS ACROSS ALL FIGURES")
print("=" * 70)

# Collect all unique Reynolds numbers
all_re_values = set()
re_file_mapping = {}

for file_num, re_val in re_time_series.items():
    all_re_values.add(re_val)
    if re_val not in re_file_mapping:
        re_file_mapping[re_val] = []
    re_file_mapping[re_val].append(file_num)

for file_num, re_val in re_cum_energy.items():
    all_re_values.add(re_val)
    if re_val not in re_file_mapping:
        re_file_mapping[re_val] = []
    if file_num not in re_file_mapping[re_val]:
        re_file_mapping[re_val].append(file_num)

for file_num, re_val in re_limit_cycle.items():
    all_re_values.add(re_val)
    if re_val not in re_file_mapping:
        re_file_mapping[re_val] = []
    if file_num not in re_file_mapping[re_val]:
        re_file_mapping[re_val].append(file_num)

# Sort and print
sorted_re = sorted(all_re_values)
for i, re_val in enumerate(sorted_re, 1):
    file_nums = sorted(set(re_file_mapping[re_val]))
    print(f"{i}. Re = {re_val:.2f}  (Files: {file_nums})")

print("\n" + "=" * 70)
print(f"Total Unique Reynolds Numbers: {len(sorted_re)}")
print("=" * 70)

# ============================================================================
# Reynolds Number Range Analysis
# ============================================================================

print("\nREYNOLDS NUMBER RANGE ANALYSIS:")
print(f"  Minimum Re: {min(sorted_re):.2f}")
print(f"  Maximum Re: {max(sorted_re):.2f}")
print(f"  Range: {max(sorted_re) - min(sorted_re):.2f}")
print(f"  Average Re: {sum(sorted_re) / len(sorted_re):.2f}")
