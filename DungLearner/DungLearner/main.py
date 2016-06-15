import dataReader
from dungLearner import dungLearner
from globalDung import globalDung
from post import post
import logging


logging.basicConfig(filename='log.log', level = logging.DEBUG, format='%(asctime)s %(message)s')
logging.getLogger("requests").setLevel(logging.WARNING)
logging.info('---------------------------------------------------------------------------------------------------------------------------------------------------------------')
logging.info('***************************************************************************************************************************************************************')
logging.info('--------------------------------------------------------------------Starting Dung Learner----------------------------------------------------------------------')
logging.info('***************************************************************************************************************************************************************')
logging.info('---------------------------------------------------------------------------------------------------------------------------------------------------------------')
logging.info('Pulling the posts from the database')

posts = dataReader.gatherReviews()

globalDungGraph = globalDung()

for idx, post in enumerate(posts):
    logging.info('----------------------------------------')
    logging.info('----------------Post' + str(idx + 1) + '-------------------')
    logging.info('----------------------------------------')
    logging.info('Review: '+ post.getReview())
    logging.info('Rating: ' + str(post.getRating()))

    dungLearnerSingle = dungLearner(post.getposExp(), post.getNegExp(), post.getSE(), post.getNoSE(), post.getSymOK(), post.getSymNOK(), post.getRating())
    weightedGraph = dungLearnerSingle.getWeightedDungGraph(globalDungGraph.getGlobalAttacksList())

    globalDungGraph.updateGlobalDung(weightedGraph)


logging.info('                                        ')
logging.info('----------------------------------------')
logging.info('---------------Summary------------------')
logging.info('----------------------------------------')
logging.info('***Node Meanings***')
logging.info('A - Positive Experience')
logging.info('B - Negative Experience')
logging.info('C - Symptoms OK')
logging.info('D - Symptoms Not OK')
logging.info('E - No Side Effects')
logging.info('F - Side Effects Present')
logging.info('                                        ')
logging.info('Attack                        Weight')   

for idx, weight in enumerate(globalDungGraph.globalWeightedGraph):

    
    logging.info(str((globalDungGraph.globalAttackList[idx])[0]) + (' -> ') + str((globalDungGraph.globalAttackList[idx])[1]) + '\t\t\t' + str(weight))


print('here')
    


