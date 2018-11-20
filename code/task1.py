"""
This module is the program for task 1.
"""
import constants
from data_extractor import DataExtractor
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from operator import itemgetter
import pickle
from util import Util

class Task1():
	def __init__(self):
		self.ut = Util()
		self.data_extractor = DataExtractor()

	def generate_imgximg_edgelist(self, image_list1, image_list2, image_feature_map, k):
		""" Method: generate_imgximg_edgelist returns image to image similarity in form of an edge list """
		imgximg_edgelist_file = open(constants.VISUALIZATIONS_DIR_PATH + "entire_graph_file.txt", "w")
		image_id_mapping_file = open(constants.DUMPED_OBJECTS_DIR_PATH + "image_id_mapping.pickle", "wb")
		image_id_mapping = {}

		for index1 in range(0, len(image_list1)):
			local_img_img_sim_list = []
			for index2 in range(0, len(image_list2)):
				image1 = image_list1[index1]
				image2 = image_list2[index2]
				features_image1 = image_feature_map[image1]
				features_image2 = image_feature_map[image2]
				score = 1 / (1 + self.calculate_similarity(features_image1, features_image2))
				imgximg_edgelist_file.write(str(image1) + " " + str(image2) + " " + str(score) + "\n")
				local_img_img_sim_list.append((image1, image2, score))
			
			self.top_k(local_img_img_sim_list, k)
			image_id_mapping[image1] = index1

		pickle.dump(["Image_id mapping:", image_id_mapping], image_id_mapping_file)
		image_id_mapping_file.close()

	def calculate_similarity(self, features_image1, features_image2):
		""" Method: image-image similarity computation"""
		return self.ut.compute_euclidean_distance(np.array(features_image1), np.array(features_image2))

	def top_k(self, graph_list, k):
		reduced_graph_file = open(constants.VISUALIZATIONS_DIR_PATH + "reduced_graph_file.txt", "a+")
		top_k = sorted(graph_list, key=lambda x:(-x[2], x[1], x[0]))[0:k]
		for iter in top_k:
			reduced_graph_file.write(str(iter[0]) + " " + str(iter[1]) + " " + str(iter[2]) + "\n")
		reduced_graph_file.close()

	def create_graph(self):
		g = nx.read_edgelist(constants.VISUALIZATIONS_DIR_PATH + "reduced_graph_file.txt", nodetype=int, \
							data=(('weight',float),), create_using=nx.DiGraph())
		print("graph created")
		return g

	def runner(self):
		"""
		Method: runner implemented for all the tasks, takes user input, and prints desired results.
		"""
		try:
			k = int(input("Enter the value of k:\t"))
			image_feature_map = self.data_extractor.prepare_dataset_for_task1(self.mapping)
			image_list = list(image_feature_map.keys())
			self.generate_imgximg_edgelist(image_list, image_list, image_feature_map, k)
		except Exception as e:
			print(constants.GENERIC_EXCEPTION_MESSAGE + "," + str(type(e)) + "::" + str(e.args))