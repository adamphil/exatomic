# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Universe Notebook Widget
#########################
To visualize a universe containing atoms, molecules, orbitals, etc., do
the following in a Jupyter notebook environment.

.. code-block:: Python

    exatomic.UniverseWidget(u)    # type(u) is exatomic.core.universe.Universe

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
#from traitlets import Unicode, link
from traitlets import Unicode
from ipywidgets import (Button, Dropdown, jslink, register, VBox, HBox,
                        IntSlider, IntRangeSlider, FloatSlider, Play,
                        FloatText, Layout, Text, Label)
from .widget_base import (ExatomicScene, UniverseScene,
                          TensorScene, ExatomicBox)
from .widget_utils import _wlo, _ListDict, Folder
from .traits import uni_traits
from exatomic.core.tensor import Tensor


class DemoContainer(ExatomicBox):
    """A proof-of-concept mixing GUI controls with a three.js scene."""
    def _field_folder(self, **kwargs):
        """Folder that houses field GUI controls."""
        folder = super(DemoContainer, self)._field_folder(**kwargs)
        fopts = Dropdown(options=['null', 'Sphere', 'Torus', 'Ellipsoid'])
        fopts.active = True
        fopts.disabled = False
        def _field(c):
            for scn in self.active():
                scn.field = c.new
        fopts.observe(_field, names='value')
        folder.insert(1, 'options', fopts)
        return folder

    def _init_gui(self, **kwargs):
        """Initialize generic GUI controls and observe callbacks."""
        mainopts = super(DemoContainer, self)._init_gui()
        geom = Button(icon='gear', description=' Mesh', layout=_wlo)
        def _geom(b):
            for scn in self.active():
                scn.geom = not scn.geom
        geom.on_click(_geom)
        mainopts.update([('geom', geom),
                         ('field', self._field_folder(**kwargs))])
        return mainopts

    def __init__(self, *scenes, **kwargs):
        super(DemoContainer, self).__init__(*scenes,
                                            uni=False,
                                            test=True,
                                            typ=ExatomicScene,
                                            **kwargs)

@register
class TensorContainer(ExatomicBox):
    """
    A simple container to implement cartesian tensor visualization.

    Args:
        file_path (string): Takes a file path name to pass through the Tensor.from_file function. Default to None.
    """
    _model_name = Unicode('TensorContainerModel').tag(sync=True)
    _view_name = Unicode('TensorContainerView').tag(sync=True)

    def _update_active(self, b):
        """
        Control which scenes are controlled by the GUI.

        Additionally align traits with active scenes so that
        the GUI reflects that correct values of active scenes.
        """
        super(TensorContainer, self)._update_active(b)
        scns = self.active()
        if not scns or len(scns) == 1: return
        carts = ['x', 'y', 'z']
        cache = {}
        for i in carts:
            for j in carts:
                tij = 't' + i + j
                cache[tij] = getattr(scns[0], tij)
        for tij, val in cache.items():
            for scn in scns[1:]:
                setattr(scn, tij, val)

    def _init_gui(self, **kwargs):
        """Initialize generic GUI controls and observe callbacks."""
        mainopts = super(TensorContainer, self)._init_gui(**kwargs)
        scn = self.scenes[0]
        alo = Layout(width='74px')
        rlo = Layout(width='235px')
        if self._df is not None:
            scn.txx = self._df.loc[0,'xx']
            scn.txy = self._df.loc[0,'xy']
            scn.txz = self._df.loc[0,'xz']
            scn.tyx = self._df.loc[0,'yx']
            scn.tyy = self._df.loc[0,'yy']
            scn.tyz = self._df.loc[0,'yz']
            scn.tzx = self._df.loc[0,'zx']
            scn.tzy = self._df.loc[0,'zy']
            scn.tzz = self._df.loc[0,'zz'] 
        xs = [FloatText(value=scn.txx , layout=alo),
              FloatText(value=scn.txy , layout=alo),
              FloatText(value=scn.txz , layout=alo)]
        ys = [FloatText(value=scn.tyx , layout=alo),
              FloatText(value=scn.tyy , layout=alo),
              FloatText(value=scn.tyz , layout=alo)]
        zs = [FloatText(value=scn.tzx , layout=alo),
              FloatText(value=scn.tzy , layout=alo),
              FloatText(value=scn.tzz , layout=alo)]
        #scale =  FloatSlider(max=10.0, step=0.01, readout=True, value=1.0)
        opt = [0] if self._df is None else [int(x) for x in self._df.index.values]
        tensorIndex = Dropdown(options=opt, value=opt[0], layout=rlo)
        tdxlabel = Label(value='Select the tensor index:')
        def _x0(c):
            for scn in self.active(): scn.txx = c.new
        def _x1(c):
            for scn in self.active(): scn.txy = c.new
        def _x2(c):
            for scn in self.active(): scn.txz = c.new
        def _y0(c):
            for scn in self.active(): scn.tyx = c.new
        def _y1(c):
            for scn in self.active(): scn.tyy = c.new
        def _y2(c):
            for scn in self.active(): scn.tyz = c.new
        def _z0(c):
            for scn in self.active(): scn.tzx = c.new
        def _z1(c):
            for scn in self.active(): scn.tzy = c.new
        def _z2(c):
            for scn in self.active(): scn.tzz = c.new
        xs[0].observe(_x0, names='value')
        xs[1].observe(_x1, names='value')
        xs[2].observe(_x2, names='value')
        ys[0].observe(_y0, names='value')
        ys[1].observe(_y1, names='value')
        ys[2].observe(_y2, names='value')
        zs[0].observe(_z0, names='value')
        zs[1].observe(_z1, names='value')
        zs[2].observe(_z2, names='value')
        rlo = Layout(width='234px')
        xbox = HBox(xs, layout=rlo)
        ybox = HBox(ys, layout=rlo)
        zbox = HBox(zs, layout=rlo)
        geom = Button(icon='cubes', description=' Geometry', layout=_wlo)

        def _change_tensor(tdx=0):
            carts = ['x','y','z']
            for i, bra in enumerate(carts):
                for j, ket in enumerate(carts):
                    if i == 0:
                        xs[j].value = self._df.loc[tdx,bra+ket]
                    elif i == 1:
                        ys[j].value = self._df.loc[tdx,bra+ket]
                    elif i == 2:
                        zs[j].value = self._df.loc[tdx,bra+ket]
            
        def _geom(b):
            for scn in self.active(): scn.geom = not scn.geom

        def _tdx(c):
            for scn in self.active(): scn.tdx = c.new
            _change_tensor(c.new)
                        
        geom.on_click(_geom)
        tensorIndex.observe(_tdx, names="value")
        mainopts.update([('geom', geom),
                         ('tlbl', tdxlabel),
                         ('tidx', tensorIndex),
                         ('xbox', xbox),
                         ('ybox', ybox),
                         ('zbox', zbox)])
        return mainopts

    def __init__(self, *args, **kwargs):
        file_path = kwargs.pop("file_path", None)
        if file_path is not None:
            self._df = Tensor.from_file(file_path)
        else:
            self._df = None
        super(TensorContainer, self).__init__(*args,
                                              uni=False,
                                              test=False,
                                              typ=TensorScene,
                                              **kwargs)


class DemoUniverse(ExatomicBox):
    """A showcase of functional forms used in quantum chemistry."""
    def _update_active(self, b):
        """
        Control which scenes are controlled by the GUI.

        Additionally align traits with active scenes so that
        the GUI reflects that correct values of active scenes.
        """
        super(DemoUniverse, self)._update_active(b)
        scns = self.active()
        if not scns: return
        flds = [scn.field for scn in scns]
        fks = [scn.field_kind for scn in scns]
        fmls = [scn.field_ml for scn in scns]
        folder = self._controls['field']
        fopts = folder['fopts'].options
        fld = flds[0]
        fk = fks[0]
        fml = fmls[0]
        if not len(set(flds)) == 1:
            for scn in scns: scn.field = fld
        if not len(set(fks)) == 1:
            for scn in scns: scn.field_kind = fk
        if not len(set(fmls)) == 1:
            for scn in scns: scn.field_ml = fml
        folder[fld].value = fk
        folder.activate(fld, enable=True)
        folder.deactivate(*[f for f in fopts if f != fld])
        if fld == 'SolidHarmonic':
            ofks = [str(i) for i in range(8) if str(i) != fk]
            folder.activate(fk, enable=True)
            folder.deactivate(*ofks)
        folder._set_gui()

    def _field_folder(self, **kwargs):
        """Folder that houses field GUI controls."""
        folder = super(DemoUniverse, self)._field_folder(**kwargs)
        uni_field_lists = _ListDict([
            ('Hydrogenic', ['1s',   '2s',   '2px', '2py', '2pz',
                            '3s',   '3px',  '3py', '3pz',
                            '3d-2', '3d-1', '3d0', '3d+1', '3d+2']),
            ('Gaussian', ['s', 'px', 'py', 'pz', 'd200', 'd110',
                          'd101', 'd020', 'd011', 'd002', 'f300',
                          'f210', 'f201', 'f120', 'f111', 'f102',
                          'f030', 'f021', 'f012', 'f003']),
            ('SolidHarmonic', [str(i) for i in range(8)])])
        kind_widgets = _ListDict([
            (key, Dropdown(options=vals))
            for key, vals in uni_field_lists.items()])
        ml_widgets = _ListDict([
            (str(l), Dropdown(options=[str(i) for i in range(-l, l+1)]))
            for l in range(8)])
        fopts = list(uni_field_lists.keys())
        folder.update(kind_widgets, relayout=True)
        folder.update(ml_widgets, relayout=True)

        def _field(c):
            fk = uni_field_lists[c.new][0]
            for scn in self.active():
                scn.field = c.new
                scn.field_kind = fk
            folder.deactivate(c.old)
            folder[c.new].value = fk
            folder.activate(c.new, enable=True)
            if c.new == 'SolidHarmonic':
                folder.activate(fk, enable=True)
            else:
                aml = [key for key in folder._get(keys=True)
                       if key.isnumeric()]
                if aml:
                    folder.deactivate(*aml)
            folder._set_gui()

        def _field_kind(c):
            for scn in self.active():
                scn.field_kind = c.new
                if scn.field == 'SolidHarmonic':
                    scn.field_ml = folder[c.new].options[0]
                    folder.activate(c.new, enable=True)
                    folder.deactivate(c.old)
                    if scn.field_ml != '0':
                        folder.deactivate('0')
                else:
                    aml = [i for i in folder._get(keys=True)
                           if i.isnumeric()]
                    if aml:
                        folder.deactivate(*aml)
            folder._set_gui()

        def _field_ml(c):
            for scn in self.active(): scn.field_ml = c.new

        for key, obj in kind_widgets.items():
            folder.deactivate(key)
            obj.observe(_field_kind, names='value')
        for key, obj in ml_widgets.items():
            folder.deactivate(key)
            obj.observe(_field_ml, names='value')
        fopts = Dropdown(options=fopts)
        fopts.observe(_field, names='value')
        folder.insert(1, 'fopts', fopts)
        folder.activate('Hydrogenic', enable=True, update=True)
        folder.move_to_end('alpha', 'iso', 'nx', 'ny', 'nz')
        return folder


    def _init_gui(self, **kwargs):
        """Initialize generic GUI controls and observe callbacks."""
        for scn in self.scenes:
            for attr in ['field_ox', 'field_oy', 'field_oz']:
                setattr(scn, attr, -30.0)
            for attr in ['field_fx', 'field_fy', 'field_fz']:
                setattr(scn, attr, 30.0)
            scn.field = 'Hydrogenic'
            scn.field_iso = 0.0005
            scn.field_kind = '1s'
        mainopts = super(DemoUniverse, self)._init_gui()
        mainopts.update([('field', self._field_folder(**kwargs))])
        return mainopts


    def __init__(self, *scenes, **kwargs):
        super(DemoUniverse, self).__init__(*scenes, uni=True, test=True,
                                           typ=ExatomicScene, **kwargs)


@register
class UniverseWidget(ExatomicBox):
    """:class:`~exatomic.container.Universe` viewing widget."""
    def _frame_folder(self, nframes):
        playable = bool(nframes <= 1)
        flims = dict(min=0, max=nframes-1, step=1, value=0)
        control = Button(description=' Animate', icon='play')
        content = _ListDict([
            ('playing', Play(disabled=playable, **flims)),
            ('scn_frame', IntSlider(description='Frame', **flims))])

        def _scn_frame(c):
            for scn in self.active(): scn.frame_idx = c.new

        content['scn_frame'].observe(_scn_frame, names='value')
        content['playing'].active = False
        jslink((content['playing'], 'value'),
               (content['scn_frame'], 'value'))
        folder = Folder(control, content)
        return folder


    def _field_folder(self, fields, **kwargs):
        folder = super(UniverseWidget, self)._field_folder(**kwargs)
        folder.deactivate('nx', 'ny', 'nz')
        fopts = Dropdown(options=fields)
        def _fopts(c):
            for scn in self.active(): scn.field_idx = c.new
        fopts.observe(_fopts, names='value')
        folder['fopts'] = fopts
        return folder

    def _iso_folder(self, folder):
        isos = Button(description=' Isosurfaces', icon='cube')
        def _fshow(b):
            for scn in self.active(): scn.field_show = not scn.field_show
        isos.on_click(_fshow)
        isofolder = Folder(isos, _ListDict([
            ('fopts', folder['fopts']),
            ('alpha', folder.pop('alpha')),
            ('iso', folder.pop('iso'))]))
        isofolder.move_to_end('alpha', 'iso')
        folder.insert(1, 'iso', isofolder, active=True)


    def _contour_folder(self, folder):
        control = Button(description=' Contours', icon='dot-circle-o')
        def _cshow(b):
            for scn in self.active(): scn.cont_show = not scn.cont_show
        control.on_click(_cshow)
        content = _ListDict([
            ('fopts', folder['fopts']),
            ('axis', Dropdown(options=['x', 'y', 'z'], value='z')),
            ('num', IntSlider(description='N', min=5, max=20,
                              value=10, step=1)),
            ('lim', IntRangeSlider(description='10**Limits', min=-8,
                                   max=0, step=1, value=[-7, -1])),
            ('val', FloatSlider(description='Value',
                                min=-5, max=5, value=0))])
        def _cont_axis(c):
            for scn in self.active(): scn.cont_axis = c.new
        def _cont_num(c):
            for scn in self.active(): scn.cont_num = c.new
        def _cont_lim(c):
            for scn in self.active(): scn.cont_lim = c.new
        def _cont_val(c):
            for scn in self.active(): scn.cont_val = c.new
        content['axis'].observe(_cont_axis, names='value')
        content['num'].observe(_cont_num, names='value')
        content['lim'].observe(_cont_lim, names='value')
        content['val'].observe(_cont_val, names='value')
        contour = Folder(control, content)
        folder.insert(2, 'contour', contour, active=True, update=True)

#    def _filter_labels(self,scn=0):
#        labels = []
#        filtered = self.active()[scn].atom_l.strip('[[')
#        filtered = filtered.strip(']]')
#        lbls = filtered.split(',')
#        for i in range(len(lbls)):
#            if lbls[i] != "":
#                labels.append(lbls[i].strip('"'))
#        return labels

    def _filter_coords(self,scn=0):
        coords = []
        filtered = [self.active()[scn].atom_x.strip('[['),
                    self.active()[scn].atom_y.strip('[['),
                    self.active()[scn].atom_z.strip('[[')]
        filtered = [filtered[0].strip(']]'),
                    filtered[1].strip(']]'),
                    filtered[2].strip(']]')]
        lbls = [filtered[0].split(','),
                filtered[1].split(','),
                filtered[2].split(',')]
        for rows in lbls:
            coords.append([])
            for cols in rows:
                if cols != "":
                    coords[-1].append(float(cols))
        return coords

    def _tensor_folder(self):
        alo = Layout(width='70px')
        rlo = Layout(width='220px')
        scale =  FloatSlider(max=10.0, step=0.001, readout=True, value=1.0)
        xs = [Text(layout=alo,disabled=True),
              Text(layout=alo,disabled=True),
              Text(layout=alo,disabled=True)]
        ys = [Text(layout=alo,disabled=True),
              Text(layout=alo,disabled=True),
              Text(layout=alo,disabled=True)]
        zs = [Text(layout=alo,disabled=True),
              Text(layout=alo,disabled=True),
              Text(layout=alo,disabled=True)]
        cs = [Text(layout=alo,disabled=True),
              Text(layout=alo,disabled=True),
              Text(layout=alo,disabled=True)]
        cidx = HBox([Text(disabled=True,description='Atom Index',layout=rlo)])
        xbox = HBox(xs, layout=rlo)
        ybox = HBox(ys, layout=rlo)
        zbox = HBox(zs, layout=rlo)
        cbox = HBox(cs, layout=rlo)
        tens = Button(description=' Tensor', icon='bank')
        tensor_cont = VBox([xbox,ybox,zbox])
        tensorIndex = Dropdown(options=[0],value=0,description='Tensor')
#        sceneIndex = Dropdown(options=[0],value=0,description='Scene')
        ten_label = Label(value="Change selected tensor:")
        sel_label = Label(value="Selected tensor in gray frame")
        cod_label = Label(value="Center of selected tensor: (x,y,z)")
        tensor = []
        self.coords = []

        def _changeTensor(tensor, tdx):
            carts = ['x','y','z']
            for i,bra in enumerate(carts):
                for j,ket in enumerate(carts):
                    tensor_cont.children[i].children[j].disabled=False
                    tensor_cont.children[i].children[j].value = \
                                            str(tensor[0][tdx][bra+ket])
                    tensor_cont.children[i].children[j].disabled=True
            adx = tensor[0][tdx]['atom']
            cidx.children[0].value = str(adx)
            cbox.children[0].value = str(self.coords[0][int(adx)])
            cbox.children[1].value = str(self.coords[1][int(adx)])
            cbox.children[2].value = str(self.coords[2][int(adx)])
#            scale.value = tensor[0][tdx]['scale']

        def _tens(c):
            for scn in self.active(): scn.tens = not scn.tens
            self.coords = self._filter_coords()
#            sceneIndex.options = [x for x in range(len(self.active()))]
#            sceneIndex.value = sceneIndex.options[0]
            tensor = self.active()[0].tensor_d
            tensorIndex.options = [x for x in range(len(tensor[0]))]
            tensorIndex.value = tensorIndex.options[0]
            tdx = tensorIndex.value
            _changeTensor(tensor, tdx)

        def _scale(c):
            for scn in self.active(): scn.scale = c.new
#            tdx = tensorIndex.value
#            tensor = self.active()[0].tensor_d
#            tensor[0][tdx]['scale'] = c.new

        def _idx(c):
            for scn in self.active(): scn.tidx = c.new
            tensor = self.active()[0].tensor_d
            tdx = c.new
            _changeTensor(tensor, tdx)

#        def _sdx(c):
#            tensor = self.active()[sceneIndex.value].tensor_d
#            tensorIndex.options = [x for x in range(len(tensor[0]))]
#            tensorIndex.value = tensorIndex.options[0]
#            tdx = tensorIndex.value
#            _changeTensor(tensor, tdx)
            
        tens.on_click(_tens)
        scale.observe(_scale, names='value')
        tensorIndex.observe(_idx, names='value')
#        sceneIndex.observe(_sdx, names='value')
        content = _ListDict([
                ('scale', scale),
                ('ten', ten_label),
#               ('sdx', sceneIndex),
                ('tdx', tensorIndex),
                ('tensor', tensor_cont),
                ('sel', sel_label),
                ('cidx', cidx),
                ('center', cod_label),
                ('coord', cbox)])
        return Folder(tens, content)

    def _init_gui(self, **kwargs):
        nframes = kwargs.pop("nframes", 1)
        fields = kwargs.pop("fields", None)
        tensors = kwargs.pop("tensors", None)
        mainopts = super(UniverseWidget, self)._init_gui(**kwargs)
        atoms = Button(description=' Fill', icon='adjust', layout=_wlo)
        axis = Button(description=' Axis', icon='arrows-alt', layout=_wlo)

        def _atom_3d(b):
            for scn in self.active(): scn.atom_3d = not scn.atom_3d

        def _axis(b):
            for scn in self.active(): scn.axis = scn.axis

        atoms.on_click(_atom_3d)
        axis.on_click(_axis)
        atoms.active = True
        atoms.disabled = False
        axis.active = True
        atoms.disabled = False
        mainopts.update([('atom_3d', atoms), ('axis', axis),
                         ('frame', self._frame_folder(nframes))])
        if fields is not None:
            folder = self._field_folder(fields, **kwargs)
            self._iso_folder(folder)
            self._contour_folder(folder)
            folder.pop('fopts')
            mainopts.update([('field', folder)])
        
        if tensors is not None:
            mainopts.update([('tensor', self._tensor_folder())])

        return mainopts

    def __init__(self, *unis, **kwargs):
        scenekwargs = kwargs.pop('scenekwargs', {})
        scenekwargs.update({'uni': True, 'test': False})
        atomcolors = scenekwargs.get('atomcolors', None)
        atomradii = scenekwargs.get('atomradii', None)
        fields, masterkwargs = [], []
        tensors = []
        for uni in unis:
            unargs, flds, tens = uni_traits(uni,
                                      atomcolors=atomcolors,
                                      atomradii=atomradii)
            tensors = tens
            fields = flds if len(flds) > len(fields) else fields
            unargs.update(scenekwargs)
            masterkwargs.append(unargs)
        nframes = max((uni.atom.nframes
                      for uni in unis)) if len(unis) else 1
        super(UniverseWidget, self).__init__(*masterkwargs,
                                             uni=True,
                                             test=False,
                                             nframes=nframes,
                                             fields=fields,
                                             typ=UniverseScene,
                                             tensors=tensors,
                                             **kwargs)