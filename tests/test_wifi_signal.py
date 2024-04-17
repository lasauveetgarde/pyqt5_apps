import os
def get_signal_level(interface:str) -> list:
    wifi_levels = {"Excellent":[0, 50, 4], "Good":[50, 60, 3], "Fair":[60, 70, 2], "Weak":[70, 100, 1]}
    lines = os.popen(f"iwconfig {interface} | grep Signal").read().split("=-")
    signal_level = int(lines[1][:2])
    for key, value in wifi_levels.items():
        if signal_level > value[0] and signal_level <= value[1]:
            return [signal_level, key, value[2]]
    return None
 
signal_level = get_signal_level("wlp9s0")
print(signal_level)