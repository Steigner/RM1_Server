# library -> image reconstruction to point cloud
import open3d as o3d

# library -> numpy data manage
import numpy as np


class Show_PointCloud(object):
    @classmethod
    def load_pc(cls, point=None, sim=False):
        if sim is True:
            pcd_o = o3d.io.read_point_cloud("app/graph/sim.pcd")

            points = np.asarray(pcd_o.points)
            colours = np.asarray(pcd_o.colors)

            cut = np.where(points[:, 2] > 1)

            points = np.delete(points, cut, axis=0)
            colours = np.delete(colours, cut, axis=0)

            s_point = [0.025268396, 0.085912548, 0.50927734]

        else:
            # color_raw = o3d.io.read_image("face.jpg")
            # depth_raw = o3d.io.read_image("face.png")

            # realworld test data
            # point = [170, 312]

            color_raw = o3d.io.read_image("app/graph/face.jpg")
            depth_raw = o3d.io.read_image("app/graph/face.png")

            imge = np.asarray(color_raw)
            imge[point[1], point[0]] = [255, 255, 255]

            print(point[1], point[0])

            color_raw = o3d.geometry.Image(imge)

            rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
                color_raw, depth_raw, convert_rgb_to_intensity=False
            )

            pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
                rgbd_image,
                o3d.camera.PinholeCameraIntrinsic(
                    o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault
                ),
            )

            k = np.asarray(pcd.colors)

            tup = np.where(
                np.logical_and(
                    k[:, 0] * 255 == 255,
                    k[:, 1] * 255 == 255,
                    k[:, 2] * 255 == 255,
                )
            )

            # tup = [6038]
            # print(tup)
            # print(pcd.points[tup[0][0]])

            # one of the possibility is set angle of motion to nostril by estimated normals
            # pcd.estimate_normals(
            #     search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

            points = np.asarray(pcd.points)
            colours = np.asarray(pcd.colors)
            normals = np.asarray(pcd.normals)

            # print(normals[tup[0]][0], normals[tup[0]][1], normals[tup[0]][2])

            s_point = pcd.points[tup[0][0]]
            # s_point = pcd.points[tup[0]]
            # s_point = [0.025268396, 0.085912548, 0.50927734]

        # this is due to color in plotly graphs
        pp_colours = colours[:] * 255.0

        # set up color of point cloud for list input to plotly.js Scatter3D
        col = [
            f"rgb({pp_colours[i,0]}, {pp_colours[i,1]}, {pp_colours[i,2]})"
            for i in range(0, int(np.size(points) / 3))
        ]

        return points[:, 0], points[:, 1], points[:, 2], col, s_point


# TESTING PURPOSE
if __name__ == "__main__":
    Show_PointCloud().load_pc()
