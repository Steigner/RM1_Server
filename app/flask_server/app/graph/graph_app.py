# --------------------- In progress !! -----------------------

import open3d as o3d
import numpy as np

class Show_PointCloud(object):
    @classmethod
    def load_pc(self):
        pcd_ = o3d.io.read_point_cloud("app/graph/multiway_registration.ply")

        points = np.asarray(pcd_.points)
        colours = np.asarray(pcd_.colors)
        normals = np.asarray(pcd_.normals)

        # cut 
        tup = np.where(
            np.logical_or( points[:,2] < -0.3, points[:,1] < -0.1 )
        )

        p_points = np.delete(points, tup, axis=0)
        p_colours = np.delete(colours, tup, axis=0)
        p_normals = np.delete(normals, tup, axis=0)

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(p_points)
        pcd.colors = o3d.utility.Vector3dVector(p_colours)
        pcd.normals = o3d.utility.Vector3dVector(p_normals)

        # this is due to color in plotly graphs
        pp_colours = p_colours[:]*255.0
        
        # set up color of point cloud for list input to plotly.js Scatter3D
        col = [f'rgb({pp_colours[i,0]}, {pp_colours[i,1]}, {pp_colours[i,2]})' for i in range(0,int(np.size(p_points)/3))]

        return p_points[:, 0], p_points[:,1], p_points[:,2], col