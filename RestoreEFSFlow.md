flowchart TD
    start(Start EFS Restoration)
    decision1{Is RecoveryPointArn Provided?}
    decision2{Is RestoreTime Provided?}
    decision3{Is Recovery Point Available for FileSystemArn?}
    success[Proceed with RecoveryPointArn]
    error1[Log Error: No Recovery Point Found Before RestoreTime]
    error2[Log Error: No Recovery Point Found]
    restore_snapshot[Call restore_efs_snapshot()]
    end[End Process]

    start --> decision1
    decision1 -- Yes --> success --> restore_snapshot --> end
    decision1 -- No --> decision2
    decision2 -- Yes --> find_closest[Find Closest Recovery Point]
    find_closest -- Recovery Point Found --> restore_snapshot
    find_closest -- No Recovery Point Found --> error1 --> end

    decision2 -- No --> decision3
    decision3 -- Yes --> retrieve_latest[Retrieve Latest Recovery Point] --> restore_snapshot
    decision3 -- No --> error2 --> end
