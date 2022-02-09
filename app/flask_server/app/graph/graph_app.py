# --------------------- In progress !! -----------------------

import open3d as o3d
import numpy as np

class Show_PointCloud(object):
    @classmethod
    def load_pc(cls, point):
        pcd_o = o3d.io.read_point_cloud("app/graph/point_cloud.ply") 
        # pcd_o = o3d.io.read_point_cloud("point_cloud.ply")        
        
        # point = [0,0,0]
        pcd_tree = o3d.geometry.KDTreeFlann(pcd_o)

        top = 1
        t = None

        for i in range(len(pcd_o.points)):
            pr = ((point[0] - pcd_o.points[i][0])**2 + (point[1] - pcd_o.points[i][1])**2 + (point[2] - pcd_o.points[i][2])**2)**(1/2)   
            if pr < top:
                top = pr
                t = i

        [k, idx, _] = pcd_tree.search_radius_vector_3d(pcd_o.points[t], 0.002)
        ktree = np.asarray(pcd_o.points)[idx[1:], :]
        ktree = np.append([pcd_o.points[t]], ktree, axis=0)
        
        """
        pcd_o.colors[point] = [1, 0, 0]
        np.asarray(pcd_o.colors)[idx[1:], :] = [0, 1, 0]
        o3d.visualization.draw_geometries([pcd_o])
        """

        """
        pcd_ = pcd_o.voxel_down_sample(voxel_size=0.01)
        
        pcd_.estimate_normals()

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pcd_.points)
        pcd.colors = o3d.utility.Vector3dVector(pcd_.colors)
        pcd.normals = o3d.utility.Vector3dVector(np.asarray(pcd_.normals))

        distances = pcd.compute_nearest_neighbor_distance()
        avg_dist = np.mean(distances)
        radius = 1.25 * avg_dist   

        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector([radius, radius * 2]))
       
        o3d.io.write_triangle_mesh("app/graph/share/test.stl", mesh)
        """
        
        points = np.asarray(pcd_o.points)
        colours = np.asarray(pcd_o.colors)
        normals = np.asarray(pcd_o.normals)

        """
        # cut 
        tup = np.where(
            np.logical_or( points[:,2] < -0.3, points[:,1] < -0.1 )
        )
        

        p_points = np.delete(points, tup, axis=0)
        p_colours = np.delete(colours, tup, axis=0)
        p_normals = np.delete(normals, tup, axis=0)
        """

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.colors = o3d.utility.Vector3dVector(colours)
        pcd.normals = o3d.utility.Vector3dVector(normals)

        # this is due to color in plotly graphs
        pp_colours = colours[:]*255.0
        
        # set up color of point cloud for list input to plotly.js Scatter3D
        col = [f'rgb({pp_colours[i,0]}, {pp_colours[i,1]}, {pp_colours[i,2]})' for i in range(0,int(np.size(points)/3))]

        return points[:, 0], points[:,1], points[:,2], col, ktree[:, 0], ktree[:, 1], ktree[:, 2]

if __name__ == "__main__":
    Show_PointCloud().load_pc()
    
    # mesh = o3d.io.read_triangle_mesh("test2.ply")

    # pcd_ = o3d.io.read_point_cloud("test.ply")

    # o3d.visualization.draw_geometries([mesh])