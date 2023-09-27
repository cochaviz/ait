#!/usr/bin/env python3

from functools import reduce
import operator

Conditionals = dict[tuple[str, str], float]
Priors = dict[str, float]

class Bayes:
    def __init__(
        self, 
        priors: Priors, 
        likelihoods: Conditionals
    ):
        self.priors = priors 
        self.likelihoods = likelihoods 

    def likelihood(self, o: str, h: str) -> float:
        return self.likelihoods[(o, h)]

    def norm_constant(self, o: str) -> float:
        return sum([ self.priors[h] * self.likelihood(o, h) for h, _ in self.priors.items() ])

    def _bayes_rule(self, h: str, o: str, norm_constant: float | None = None) -> float:
        if norm_constant is None:
            norm_constant = self.norm_constant(o) 

        return self.priors[h] * self.likelihood(o, h) / norm_constant

    def single_posterior_update(self, o: str) -> Priors:
        norm_constant = self.norm_constant(o)

        return { h : self._bayes_rule(h, o, norm_constant=norm_constant) 
                for h, _ in self.priors.items() }

def steal_cookie_jar():
    return Bayes(
        priors = {
            "bowl1" : .5, 
            "bowl2" : .5
        },
        likelihoods = { 
            ( "vanilla", "bowl1" ) : 35/50,
            ( "chocolate", "bowl1" ) : 15/50,
            ( "vanilla", "bowl2" ) : 20/50,
            ( "chocolate", "bowl2" ) : 30/50,
        }
    )

def watch_archer():
    return Bayes(
        priors = {
            "beginner" : 1/4,
            "intermediate" : 1/4,
            "advanced" : 1/4,
            "expert" : 1/4,
        },
        likelihoods= {
            ("yellow", "beginner") : .5,
            ("yellow", "intermediate") : .1,
            ("yellow", "advanced") : .2,
            ("yellow", "expert") : .3,

            ("red", "beginner") : .1,
            ("red", "intermediate") : .2,
            ("red", "advanced") : .4,
            ("red", "expert") : .5,

            ("blue", "beginner") : .4,
            ("blue", "intermediate") : .4,
            ("blue", "advanced") : .25,
            ("blue", "expert") : .125,

            ("black", "beginner") : .25,
            ("black", "intermediate") : .2,
            ("black", "advanced") : .1,
            ("black", "expert") : .05,

            ("white", "beginner") : .2,
            ("white", "intermediate") : .1,
            ("white", "advanced") : .05,
            ("white", "expert") : .025,
        }
    )

def question_1():
    cookie_jar = steal_cookie_jar()
    print(f"Question 1: {cookie_jar.single_posterior_update('vanilla')['bowl1']}")

def question_2():
    cookie_jar = steal_cookie_jar()

    chocolate_cookie = cookie_jar.single_posterior_update('chocolate')
    vanilla_cookie = cookie_jar.single_posterior_update('vanilla')
    
    print(f"Question 2: {vanilla_cookie['bowl2'] * chocolate_cookie['bowl2']}") 

def archer_level_likelihoods() -> Priors:
    archer = watch_archer()
    observations = ["yellow", "white", "red", "red", "blue"]
    posteriors: list[Priors] = []

    for o in observations:
        posteriors.append(archer.single_posterior_update(o))

    level_likelihoods: Priors = {}

    for level in archer.priors.keys():
        level_likelihoods[level] = reduce(operator.mul, [ p[level] for p in posteriors ]) 

    return level_likelihoods

def question_3():
    print(f"Question 3: {archer_level_likelihoods()['intermediate']}")

def question_4():
    level_likelihoods = archer_level_likelihoods()
   
    print(f"Question 4: {max(level_likelihoods, key=level_likelihoods.get)}") # type: ignore

if __name__=="__main__":
    question_1()
    question_2()
    question_3()
    question_4()