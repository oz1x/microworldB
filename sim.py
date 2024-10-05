import world
import aiA
import aiB
import display
import time

DIRECTIONS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0)
}

FACINGS = ['N', 'E', 'S', 'W']
VALID_COMMANDS = [
    'N', # Move north
    'E', # Move east
    'W', # Move west
    'S', # Move south
    'U' # Teleport/Open Door/Touch Goal
]


def run_sim(
    the_world, 
    max_turns=None, 
    log=None, 
    use_display=False,
    display_speed=0.5
):

    POINTS_PER_GOAL = 0
    if max_turns is not None:
        POINTS_PER_GOAL = max_turns
    
    the_aiA = aiA.AI(max_turns)
    the_aiB = aiB.AI(max_turns)

    agent_xA, agent_yA = the_world.get_startxyA()
    agent_xB, agent_yB = the_world.get_startxyB()
    agent_facingA = the_world.get_start_face_dirA()
    agent_facingB = the_world.get_start_face_dirB()
    cells_visited = []
    turn = 1
    agent_cmdA = "X"
    agent_cmdB = "X"
    msgA = None
    msgB = None
    perceptsA = {}
    perceptsB = {}
    pointsA = 0
    pointsB = 0
    aiA_state = 'GOOD'
    aiB_state = 'GOOD'

    disp = None

    if use_display:
        import display
        disp = display.Display(
            the_world,
            agent_xA,
            agent_yA,
            agent_xB,
            agent_yB
        )

    if use_display:
        disp.update(
            agent_xA,
            agent_yA,
            agent_facingA,
            agent_xB,
            agent_yB,
            agent_facingB
        )
        time.sleep(display_speed)

    

    run = True
    while run:

        
        if aiA_state != 'GOOD' and aiB_state != 'GOOD':
            run = False
            write_to_log(
                log,
                f"-----Scenario finished-----"
            )
            write_to_log(
                log,
                f"FINAL AGENT STATES:\nAgent A {aiA_state}\nAgent B {aiB_state}"
            )
            continue
        else:
            write_to_log(
                log,
                f"-----Turn {turn}-----"
            )
        
        if aiA_state == 'GOOD':
            pointsA += 1
            
            # What does the agent see?
            perceptsA = get_percepts(the_world, agent_xA, agent_yA, agent_facingA)
            
            # Get agent's command
            agent_cmdA, msgA = the_aiA.update(perceptsA, msgB)
            
            # LOG ###############################################################
            
            write_to_log(
                log,
                f"Agent A"
            )
            write_to_log(
                log,
                f"   Start:    {agent_xA},{agent_yA}"
            )
            percept_str = ""
            for k, v in perceptsA.items():
                percept_str += f"({k} {v}) "
            write_to_log(
                log,
                f"   Percepts: {percept_str}"
            )
            write_to_log(
                log,
                f"   Command:  {agent_cmdA}"
            )

            # ####################################################################

            # Move the agent
            if validate_agent_cmd(agent_cmdA):

                new_agent_x = agent_xA
                new_agent_y = agent_yA

                match agent_cmdA:
                    case 'N' | 'E' | 'S' | 'W':
                        dx, dy = DIRECTIONS[agent_cmdA]
                        new_agent_x = agent_xA + dx
                        new_agent_y = agent_yA + dy
                        if the_world.is_cell_enterable(new_agent_x, new_agent_y):
                            agent_xA = new_agent_x
                            agent_yA = new_agent_y


                trigger = the_world.check_triggers(agent_xA, agent_yA, agent_cmdA)
                match trigger[0]:
                    case "EXIT":
                        write_to_log(
                            log,
                            f"   Trigger:  Agent A has left the environment."
                        )
                        aiA_state = 'EXITED'
                        agent_xA = None
                        agent_yA = None
                        agent_facingA = None
                    case "TELEPORT":
                        write_to_log(
                            log,
                            f"   Trigger:  Agent A teleported from {the_world.get_cell(agent_xA, agent_yA)} to {the_world.get_cell(trigger[1], trigger[2])}"
                        )
                        agent_xA = trigger[1]
                        agent_yA = trigger[2]

                    case "GOAL_TRIGGERED":
                        # if trigger[1] == 0:
                        #     write_to_log(
                        #         log,
                        #         f"   Trigger:  Agent A activated goal {trigger[2]}"
                        #     )
                        #     write_to_log(
                        #         log,
                        #         f"   Trigger:  Your team has completed this map in {turn} turns. SUCCESS"
                        #     )
                        #     run = False
                        # else:
                        pointsA += POINTS_PER_GOAL
                        write_to_log(
                            log,
                            f"   Trigger:  Agent A activated goal {trigger[2]}"
                        )
                    case "NONE":
                        pass


                write_to_log(
                    log,
                    f"   End:      {agent_xA},{agent_yA}"
                )

            else:
                write_to_log(log, f"Agent A invalid command: {agent_cmdA}")
                write_to_log(log, "Agent A - FAILURE")
                aiA_state = 'BAD'

        if aiB_state == 'GOOD':
            pointsB += 1
            
            # What does the agent see?
            perceptsB = get_percepts(the_world, agent_xB, agent_yB, agent_facingB)

            # Get agent's command
            agent_cmdB, msgB = the_aiB.update(perceptsB, msgA)

            # LOG ###############################################################
            write_to_log(
                log,
                f"Agent B"
            )
            write_to_log(
                log,
                f"   Start:    {agent_xB},{agent_yB}"
            )
            percept_str = ""
            for k, v in perceptsB.items():
                percept_str += f"({k} {v}) "
            write_to_log(
                log,
                f"   Percepts: {percept_str}"
            )
            write_to_log(
                log,
                f"   Command:  {agent_cmdB}"
            )

            # ####################################################################

            # Move the agent
            if validate_agent_cmd(agent_cmdB):

                new_agent_x = agent_xB
                new_agent_y = agent_yB

                match agent_cmdB:
                    case 'N' | 'E' | 'S' | 'W':
                        dx, dy = DIRECTIONS[agent_cmdB]
                        new_agent_x = agent_xB + dx
                        new_agent_y = agent_yB + dy
                        if the_world.is_cell_enterable(new_agent_x, new_agent_y):
                            agent_xB = new_agent_x
                            agent_yB = new_agent_y


                trigger = the_world.check_triggers(agent_xB, agent_yB, agent_cmdB)
                match trigger[0]:
                    case "EXIT":
                        write_to_log(
                            log,
                            f"   Trigger:  Agent B has left the environment."
                        )
                        aiB_state = 'EXITED'
                        agent_xB = None
                        agent_yB = None
                        agent_facingB = None
                    case "TELEPORT":
                        write_to_log(
                            log,
                            f"   Trigger:  Agent B teleported from {the_world.get_cell(agent_xB, agent_yB)} to {the_world.get_cell(trigger[1], trigger[2])}"
                        )
                        agent_xB = trigger[1]
                        agent_yB = trigger[2]

                    case "GOAL_TRIGGERED":
                        # if trigger[1] == 0:
                        #     write_to_log(
                        #         log,
                        #         f"   Trigger:  Agent B activated goal {trigger[2]}"
                        #     )
                        #     write_to_log(
                        #         log,
                        #         f"   Trigger:  Your team has completed this map in {turn} turns. SUCCESS"
                        #     )
                        #     run = False
                        # else:
                        pointsB += POINTS_PER_GOAL
                        write_to_log(
                            log,
                            f"   Trigger:  Agent B activated goal {trigger[2]}"
                        )
                    case "NONE":
                        pass


                write_to_log(
                    log,
                    f"   End:      {agent_xB},{agent_yB}"
                )


            else:
                write_to_log(log, f"Agent B invalid command: {agent_cmdB}")
                write_to_log(log, "Agent B - FAILURE")
                aiB_state = 'BAD'
            

        if use_display:
            disp.update(
                agent_xA,
                agent_yA,
                agent_facingA,
                agent_xB,
                agent_yB,
                agent_facingB
            )
            time.sleep(display_speed)

        if max_turns is not None:
            if turn >= max_turns:
                write_to_log(
                    log,
                    f"---MAX TURNS REACHED---"
                )
                run = False
                continue
            
        turn += 1


    A_points_scored = pointsA if aiA_state == 'EXITED' else 0
    B_points_scored = pointsB if aiB_state == 'EXITED' else 0
        
    write_to_log(
        log,
        f"\nFINAL SCORE"
    )
    write_to_log(
        log,
        f"Agent A received {pointsA} points and scored {A_points_scored} points."
    )
    write_to_log(
        log,
        f"Agent B received {pointsB} points and scored {B_points_scored} points."
    )
    write_to_log(
        log,
        f"TOTAL: {A_points_scored + B_points_scored}"
    )
        
    if use_display:
        disp.quit()

def get_percepts(the_world, agent_x, agent_y, agent_facing):
    # percepts = the_world.get_cells_around(agent_x, agent_y)
    percepts = {'X':[the_world.get_cell(agent_x, agent_y)]}
    for d, v in DIRECTIONS.items():
        dx, dy = v
        ray = the_world.raycast(agent_x, agent_y, dx, dy)
        ray = the_world.prune_raycast(ray)
        percepts[d] = ray

    # percepts = [the_world.get_cell(agent_x, agent_y)]
    # dx, dy = DIRECTIONS[agent_facing]
    # ray = the_world.raycast(
    #     agent_x,
    #     agent_y,
    #     dx, dy
    # )
    # ray = the_world.prune_raycast(ray)
    # percepts += ray
    return percepts


def validate_agent_cmd(cmd):
    return cmd in VALID_COMMANDS

def write_to_log(log, msg):
    if log is not None:
        log.write(f"{msg}\n")
        log.flush()
    else:
        print(msg)

def turn_right(cur_facing):
    match cur_facing:
        case 'N': return 'E'
        case 'E': return 'S'
        case 'S': return 'W'
        case 'W': return 'N'

def turn_left(cur_facing):
    match cur_facing:
        case 'N': return 'W'
        case 'W': return 'S'
        case 'S': return 'E'
        case 'E': return 'N'
