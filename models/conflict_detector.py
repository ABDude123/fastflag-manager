class ConflictDetector:
    def __init__(self):
        self.conflicting_pairs = {
            ("FFlagDisableSpeculativeGPUMemoryAllocation", "FFlagEnableGPUAcceleration"),
            ("DFIntTaskSchedulerTargetFps", "DFIntGameThreadCount")
        }
        
    def check_conflicts(self, active_flags):
        conflicts = []
        for flag1, flag2 in self.conflicting_pairs:
            if flag1 in active_flags and flag2 in active_flags:
                conflicts.append((flag1, flag2))
        return conflicts 