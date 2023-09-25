from modeller import *
from modeller.automodel import *

env = Environ()      
a = AutoModel(env, alnfile='model-template.ali',                                        
              knowns='template', sequence='model',                                                                                
			  assess_methods=(assess.DOPE,          
			                  #soap_protein_od.Scorer(),  
							  assess.GA341))       
a.starting_model = 1          
a.ending_model = 5   
a.make()       
