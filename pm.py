import pandas as pd

import networkx as nx
import matplotlib.pyplot as plt


# Read the event log data into a DataFrame
event_log_data = pd.read_csv('AnonymizedEventData.csv', sep=',')

# Group the events by TicketNum and create a list of traces
traces = event_log_data.groupby('TicketNum').apply(lambda x: x['Status'].tolist()).tolist()

# Display the multi-set of traces L
for trace in traces:
    print(trace)
    
# Create a set of unique event types
event_types = set(event_log_data['Status'])

# Display the set TL
print(event_types)

# Get the first and last events of each trace
start_events = [trace[0] for trace in traces]
end_events = [trace[-1] for trace in traces]

# Display the start and end events
print("Start events:", start_events)
print("End events:", end_events)

# Create a set of unique event patterns
event_patterns = set(zip(start_events, end_events))

# Display the set PL
print(event_patterns)

# Count the frequency of each event pattern
event_pattern_freqs = {pattern: traces.count(list(pattern)) for pattern in event_patterns}

# Display the set FL
print(event_pattern_freqs)

# Sort the event patterns based on their frequencies in descending order
sorted_patterns = sorted(event_pattern_freqs.items(), key=lambda x: x[1], reverse=True)

# Extract the resultant process from the most frequent event pattern
resultant_process = list(sorted_patterns[0][0])

# Display the resultant process
print(resultant_process)










# Simulate the execution of the discovered process
simulated_traces = []
for i in range(len(traces)):
    simulated_trace = [resultant_process[0]]
    for j in range(len(traces[i]) - 1):
        current_event = simulated_trace[-1]
        if current_event == resultant_process[-1]:
            simulated_trace.append(current_event)
        else:
            next_event = resultant_process[resultant_process.index(current_event) + 1]
            simulated_trace.append(next_event)
    simulated_traces.append(simulated_trace)

# Calculate the fitness by counting the number of matching events
total_events = sum(len(trace) for trace in traces)
matching_events = sum(len(set(simulated_trace) & set(actual_trace)) for simulated_trace, actual_trace in zip(simulated_traces, traces))
fitness = matching_events / total_events

# Display the fitness
print("Fitness:", fitness)





# Define the resultant process
# resultant_process = ['Open', 'Open']

# Create a directed graph
graph = nx.DiGraph()

# Add nodes and edges to the graph
for i in range(len(resultant_process) - 1):
    source_event = resultant_process[i]
    target_event = resultant_process[i + 1]
    graph.add_edge(source_event, target_event)

# Set node positions for better visualization
pos = nx.spring_layout(graph)

# Draw the graph
nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, edge_color='gray', arrows=True)

# Set plot title and display the graph
plt.title('Resultant Process')
plt.axis('off')
plt.show()