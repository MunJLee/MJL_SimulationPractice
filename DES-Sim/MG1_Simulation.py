"""
Discrete Event Simulator - M/G/1 Queue

written in python3 ver. 3.6.8
(in order to run, type 'python3 MG1_Simulation.py' from commandline)


NOTE: numpy package must be installed through pip3 prior
"""

#import packages
import numpy as np




#global variables
TRIAL_RUNS = 10
TOTAL_PEOPLE_SERVED = 100

POISSON_INPUT = 1
GAMMA_ALPHA_INPUT = 3
GAMMA_BETA_INPUT = 0.25


def main():

    currentTrial = 0
    trialAverageQueueLength = []    #IN CASE i NEED TO MAKE A GRAPH


    while currentTrial != TRIAL_RUNS:

        print("\nTRAIL#:", currentTrial + 1)

        queueCounter = 0
        currentClock = 0.0

        nextArrivalEvent = 0.0
        nextDepartureEvent = 0.0

        serviceCompletion = 0

        arrivalTimeRecorder = []
        sojournTimeRecorder = []
        queueDurationRecorder = [0.0]

        queueLengthRecord = [0]     #IN CASE I NEED TO MAKE A GRAPH



        #initialization, by creating the first arrival event
        nextArrivalEvent = generateArrivalEvent(POISSON_INPUT)
        print("FIRST EVENT:", nextArrivalEvent)


        #until the target amount of customers are served
        while serviceCompletion != TOTAL_PEOPLE_SERVED:

            #determine if the event is arrival or departure
            if (nextDepartureEvent == 0.0) or (nextDepartureEvent != 0.0 and nextArrivalEvent <= nextDepartureEvent):

                #IF IT IS ARRIVAL
                print("\nARRIVAL ")

                #use current queue counter as index to enter duration into into queueDurationRecorder
                if nextArrivalEvent == 0.0:
                    #A case of more than one arrival happening at once (I think)
                    cumulativeDuration = round(queueDurationRecorder[queueCounter] + 0.0, 1)
                else:
                    cumulativeDuration = round(queueDurationRecorder[queueCounter] + (nextArrivalEvent - currentClock), 1)

                queueDurationRecorder[queueCounter] = float(cumulativeDuration)

                #set clock to the event time
                currentClock = nextArrivalEvent

                #+1 for queue counter
                queueCounter += 1
                queueLengthRecord.append(queueCounter)

                if len(queueDurationRecorder) == queueCounter:
                    queueDurationRecorder.append(0.0)

                #enter the event time into arrivalEventRecorder
                arrivalTimeRecorder.append(currentClock)

                #generate next arrival event
                nextArrivalEvent = currentClock + generateArrivalEvent(POISSON_INPUT)


                #there is no next departure event [=server idle], generate next departure event too
                if nextDepartureEvent == 0.0:
                    nextDepartureEvent = round(currentClock + generateServiceTime(GAMMA_ALPHA_INPUT, GAMMA_BETA_INPUT), 1)


                eventSummary(queueCounter, currentClock, nextArrivalEvent, cumulativeDuration, arrivalTimeRecorder,
                             sojournTimeRecorder, queueDurationRecorder)



            else:

                #IF IT IS DEPARTURE
                print("\nDEPARTURE ")

                #use current queue counter as index to enter duration into into queueDurationRecorder
                cumulativeDuration = round(queueDurationRecorder[queueCounter] + (nextDepartureEvent - currentClock),1)
                queueDurationRecorder[queueCounter] = float(cumulativeDuration)

                #set clock to the event time
                currentClock = nextDepartureEvent

                #-1 for queue counter
                queueCounter -= 1
                queueLengthRecord.append(queueCounter)

                #enter the calculate departure time into sojournRecorder
                sojournTimeRecorder.append(round(currentClock - arrivalTimeRecorder[serviceCompletion], 1))

                #+1 for serviceCompletion
                serviceCompletion += 1

                #if queue is not empty then generate next departure event; otherwise, set nextDepartureEvent as 0.0 [idle]
                if queueCounter != 0:
                    nextDepartureEvent = round(currentClock + generateServiceTime(GAMMA_ALPHA_INPUT, GAMMA_BETA_INPUT), 1)

                else:
                    nextDepartureEvent = 0.0


                eventSummary(queueCounter, currentClock, nextDepartureEvent, cumulativeDuration, arrivalTimeRecorder,
                             sojournTimeRecorder, queueDurationRecorder)



        # simulation summary
        trialAverageQueueLength.append(simulationSummary(currentClock, arrivalTimeRecorder, sojournTimeRecorder,
                                                         queueDurationRecorder))

        currentTrial += 1


    #final tally
    print("\nAVERAGE QUEUE LENGTH FOR ALL TRIAL:", trialAverageQueueLength)





def generateArrivalEvent(lambdaInput):

    #generate random variable from Poisson distribution
    rvCreated = np.random.poisson(lambdaInput, 1)

    eventValue = float(rvCreated[0])
    #print("ARRIVAL EVENT VALUE BEING RETURNED:", eventValue)
    return eventValue




def generateServiceTime(alphaInput, betaInput):

    #generate random variable from Gamma distribution
    rvCreated = np.random.gamma(alphaInput, betaInput, 1)

    eventValue = float(round(rvCreated[0], 1))
    #print("DEPARTURE EVENT VALUE BEING RETURNED:", eventValue)
    return eventValue



def eventSummary(counter, systemClock, nextEvent, duration, arrivalRecord, departureRecord, queueStatus):
    print("QUEUE COUNTER", counter)
    print("CURRENT CLOCK", systemClock)
    print("NEXT EVENT", nextEvent)
    print("CUMULATIVE DURATION", duration)
    print("ARRIVAL TIME RECORDER", arrivalRecord)
    print("SYSTEM DURATION RECORDER", departureRecord)
    print("QUEUE DURATION RECORDER", queueStatus)


def simulationSummary(systemClock, arrivalRecord, departureRecord, queueStatus):
    print("\nFINAL CLOCK", systemClock)
    print("ARRIVAL TIME RECORDER:", arrivalRecord)
    print("SOJOURN TIME RECORDER:", departureRecord)
    print("QUEUE DURATION RECORDER", queueStatus)

    queueLevel = 0
    sumOfDuration = 0
    for duration in queueStatus:
        sumOfDuration += (queueLevel * duration)
        queueLevel += 1

    averageQueueLength = round(sumOfDuration / systemClock, 2)
    print("\nMEAN QUEUE LENGTH:", averageQueueLength)

    return averageQueueLength



if __name__ == '__main__':
    main()
    #add charting capability if you can
