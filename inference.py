from pyswip import Prolog

def clean_theory(theory):
    clean_theory = []
    for i in range(0,len(theory)-1):
        if ':-' not in theory[i+1]:
                rule = theory[i].strip().replace('\n', '') + ' ' + theory[i+1].strip().replace('\n', '')
                clean_theory.append(rule)
    
    return clean_theory

def merge_lines(clean_theory):
    # Tidy up to ensure all rules begin with head :- body
    full_theory = []
    if len(clean_theory) > 1:
        for i in range(0,len(clean_theory)-1):
            if ':-' not in clean_theory[i+1]:
                    rule = clean_theory[i] + ' ' + clean_theory[i+1]
                    full_theory.append(rule)
            elif ':-' in clean_theory[i]:
                full_theory.append(clean_theory[i])

    else:
        full_theory = clean_theory

    return full_theory

def add_variable(full_theory):
    new_theory = []
    for rule in full_theory:
        head = 'true_class(A,EX) :-'
        body = rule.rpartition(':-')[2][:-1]

        new_body = body + ', Ex = ' + f'({body}).'
        new_clause = head + new_body

        new_theory.append(new_clause)
    
    return new_theory
    
def save_ruleset_to_prolog(dataset, filename, full_theory):
    file = open(filename, 'w')
    file.write(f':-consult("aleph_input/{dataset}_aleph.bk").\n')
    file.write("\n")

    for rule in full_theory:
        head = 'true_class(A,Ex) :-'
        body = rule.rpartition(':-')[2][:-1]

        file.write(head + "\n")
        file.write("    " + body + ",\n")
        file.write("    Ex = " + f"[{body.strip()}].\n")
        file.write("\n")

    file.close()        

def translate_theory(dataset, filename = 'working_theory.pl'):

    with open(f'{dataset}_theory.txt') as f:
        theory = f.readlines()
    
    theory = clean_theory(theory)
    theory = merge_lines(theory)
    save_ruleset_to_prolog(dataset, filename, theory)
    return theory

def single_instance_inference(dataset, example_number, prolog):
    # theory = translate_theory(dataset = dataset)
    prolog.consult("working_theory.pl")
    result = list(prolog.query(f"true_class(example_{example_number}, Explanation)"))

    # Extract prediction and explanation
    if len(result) == 0:
        pred = 'Negative Class'
        explanation = None
    elif len(result) == 1:
        pred = 'Positive Class'
        explanation = result[0]['Explanation']
    else: # need to fix this - why is some len 1 and others more?
        pred = 'Positive Class'
        explanation = result[0]['Explanation']

    return (pred, explanation)

def add_constraint(dataset, constraint_predicate):
    """Currently just removes a predicate from a theory"""
    output_directory = 'aleph_input'
    bk_file = open(output_directory + '/' + dataset + '_aleph.bk', 'a')
    bk_file.write(f"false :- hypothesis(_,Body,_), bodyList(Body, List), !, member({constraint_predicate}, List).\n\n")
    
    bk_file.close()

def ilp_induce(dataset, prolog):
    # generate initial ILP thoery and save to a file
    prolog.consult('aleph6.pl')
    list(prolog.query(f"read_all('aleph_input/{dataset}_aleph')."))
    list(prolog.query("induce."))
    list(prolog.query(f"write_rules('{dataset}_theory.txt')."))