import numpy as np
import pyvista as pv

# This function is replaced by affine_transform_matrix in geometron.geometries.transforms
# def vtk_transform_matrix_from_control_points(origin_coords, destination_coords, rcond=-1):
#     """ Computes a 4x4 transform matrix to use on vtk objects from control points
#     Parameters
#     ----------
#     origin_coords : numpy.array
#         3D coordinates of the control points in the origin space
#     destination_coords : numpy.array
#         3D coordinates of the control points in the destination space
#     rcond : float, default: -1
#         Cut-off ratio for small singular values used by numpy.linalg.lstsq
#     Returns
#     -------
#     matrix : numpy.array
#         The 4x4 transform matrix
#     residuals : numpy.array
#         The residuals of the least-squares fitting of the parameters of the transform from the control points
#         coordinate pairs
#     """
#     a = np.vstack([np.array(origin_coords).T, np.array([1., 1., 1., 1.])]).T
#     b = np.array(destination_coords)
#     transform_matrix, residuals, rank, singular = np.linalg.lstsq(a, b, rcond=rcond)
#     return np.vstack([transform_matrix.swapaxes(0, 1), np.array([0., 0., 0., 1.])]), residuals


def transform_vtk(transform_matrix, infile, outfile=None):
    """ Transforms a vtk file using an affine transform in 3D defined by the transform matrix
    Parameters
    ----------
    transform_matrix : numpy.ndarray
        a 4x4 affine transform matrix
    infile: str or path
        filename of a vtk file to transform
    outfile: str or path
        filename of the transformed vtk file
    """

    # TODO: if a 3x3 matrix is passed convert it to a (4x4) transform matrix with rotation on the z-axis
    #  and translations along the x and y-axis or take an optional argument to specify around which axis the rotation should be done
    if np.shape(transform_matrix) == (4, 4):
        vtk_obj = pv.read(infile)
        vtk_obj.transform(transform_matrix)
        if outfile is None:
            outfile = infile[:-4] + '_3D.vtk'
        pv.save_meshio(outfile, vtk_obj)
    else:
        print('invalid transform matrix')

def map_image_to_plane(image_file, vtk_transform_matrix, flip_lr=False, flip_ud=False):
    image = pv.read_texture(image_file)
    sx, sy = image.dimensions
    x = np.arange(0., sx, 1.)
    y = np.arange(0., sy, 1.)
    z = 0.
    mx, my, mz = np.meshgrid(x, y, z)
    section_plane = pv.StructuredGrid(mx, my, mz)
    section_plane.transform(vtk_transform_matrix)
    origin=[section_plane.bounds[0], section_plane.bounds[2], section_plane.bounds[4]]
    point_u=[section_plane.bounds[0], section_plane.bounds[3], section_plane.bounds[4]]
    point_v=[section_plane.bounds[0], section_plane.bounds[2], section_plane.bounds[5]]
    if flip_lr:
        origin[1]=section_plane.bounds[3]
        point_u[1]=section_plane.bounds[2]
        point_v[1]=section_plane.bounds[3]
    if flip_ud:
        origin[2]=section_plane.bounds[5]
        point_u[2]=section_plane.bounds[5]
        point_v[2]=section_plane.bounds[4]
    section_plane = section_plane.texture_map_to_plane(origin=origin, point_u=point_u, point_v=point_v, use_bounds=False)
    return section_plane, image