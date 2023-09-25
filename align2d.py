from modeller import *

env = Environ()
aln = Alignment(env)
mdl = Model(env, file='template', model_segment=('FIRST:A','LAST:A'))
aln.append_model(mdl, align_codes='template', atom_files='template.pdb')
aln.append(file='model.ali', align_codes='model')                                                                                
aln.align2d(max_gap_length=50)                                   
aln.write(file='model-template.ali', alignment_format='PIR')                                                                                                                                            
aln.write(file='model-template.pap', alignment_format='PAP')  
########  
