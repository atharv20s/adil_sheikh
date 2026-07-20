import re

with open('thesis/thesis_main.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Add missing properties to PBFT if not present
pbft_properties = r'''
\subsection{Properties}
\begin{itemize}
    \item \textbf{Safety:} Guaranteed if  \ge 3f + 1$, under cryptographic assumptions. Two conflicting requests will never commit at the same sequence number because a commit certificate requires +1$ identical prepares, meaning at least +1$ honest nodes prepared it, which is a majority of the honest nodes.
    \item \textbf{Liveness:} Guaranteed under partial synchrony after GST, as the view-change mechanism ensures progression when a primary is faulty.
    \item \textbf{Termination:} A valid request initiated by a client will eventually be processed and the result returned.
\end{itemize}

'''

# I will just write a function to inject this after Message Complexity for PBFT, Tower, and RVR if it doesn't exist
def inject_properties(content, algo_name, props):
    if props[:20] not in content:
        # Find where to inject
        if f'\subsection{{Message Complexity}}' in content.split(algo_name)[1][:2000]:
            # Inject after the Message Complexity section of the current algorithm
            start_idx = content.find(algo_name)
            if start_idx != -1:
                # Find the next section or subsection after Message Complexity
                msg_complex_idx = content.find(r'\subsection{Message Complexity}', start_idx)
                if msg_complex_idx != -1:
                    next_sec_idx = content.find(r'\section', msg_complex_idx)
                    next_subsec_idx = content.find(r'\subsection', msg_complex_idx + 10)
                    end_idx = min(idx for idx in [next_sec_idx, next_subsec_idx, len(content)] if idx != -1)
                    
                    content = content[:end_idx] + props + content[end_idx:]
    return content

content = inject_properties(content, r'\section{Classic PBFT}', pbft_properties)

tower_properties = r'''
\subsection{Properties}
\begin{itemize}
    \item \textbf{Safety:} Maintains safety up to  = \lfloor (n-1)/3 \rfloor$ malicious nodes, relying on threshold signatures to aggregate votes and verifiable random functions to randomly select a committee.
    \item \textbf{Liveness:} Guaranteed by rotating the primary through a verifiable random function mechanism, reducing primary censorship.
    \item \textbf{Termination:} Transactions are finalized deterministically once the threshold signature is assembled for a block.
\end{itemize}

'''
content = inject_properties(content, r'\section{Tower BFT}', tower_properties)

rvr_properties = r'''
\subsection{Properties}
\begin{itemize}
    \item \textbf{Safety:} Guaranteed under standard +1$ conditions. By integrating reputation, RVR increases the economic cost of a safety violation, effectively making the threshold {effective} < f$.
    \item \textbf{Liveness:} Accelerated by the reputation-weighted primary selection, ensuring that highly reputable (and likely performant) nodes are chosen more frequently.
    \item \textbf{Termination:} Terminating conditions are identical to PBFT, modulo the reputation decay function that penalizes non-responsive validators.
\end{itemize}

'''
content = inject_properties(content, r'\section{RVR Consensus}', rvr_properties)

with open('thesis/thesis_main.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Properties injected.")
