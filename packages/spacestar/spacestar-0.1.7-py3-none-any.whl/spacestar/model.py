from __future__ import annotations

import io

from anyio import create_task_group
from ormspace import model as md
from ormspace.model import getmodel
from starlette.requests import Request
from typing_extensions import Self

from hx_markup import Element


@md.modelmap
class SpaceModel(md.Model):
    
    def set_dependencies(self):
        for k, v in self.model_fields.items():
            if k in self.key_field_names():
                fd = getattr(self, k)
                fd.set_instance(getmodel(self.instance_name_for(k)).Database.instance_from_context(fd.key))
            elif k in self.tablekey_field_names():
                if tk:= getattr(self, k):
                    tk.set_instance(tk.table).Database.instance_from_context(tk.key)
                    
    async def update_instance_context(self):
        data = self.asjson()
        async with create_task_group() as tks:
            for m in self.dependencies():
                if m.model_key_name() in data:
                    query = {'key': data[m.model_key_name()]}
                    print(query)
                    tks.start_soon(m.update_model_context, False, query)
        self.set_dependencies()
    
    @classmethod
    async def fetch_instance(cls, key: str) -> Self:
        return cls(**await cls.fetch_one(key))
    
    @property
    def tablekey(self) -> str:
        return f'{self.table()}.{self.key}'
    
    @property
    def table_key(self) -> str:  #TODO: deletar
        return self.tablekey
    
    @classmethod
    def field(cls, name: str):
        return cls.model_fields.get(name, None)
    
    async def display(self):
        with io.StringIO() as f:
            container: Element = Element('div', id=self.table_key)
            container.children.append(Element('h3', children=str(self)))
            container.children.append(Element('ul', '.nav', children=[Element('li','.nav-item', children=f'{k}: {v}') for k, v in dict(self).items()]))
            f.write(str(container))
            return f.getvalue()
        
    async def heading(self, tag: str, *args, **kwargs):
        with io.StringIO() as f:
            kwargs['children'] = str(self)
            f.write(str(Element(tag, *args, **kwargs)))
            return f.getvalue()
        
    @classmethod
    def query_from_request(cls, request: Request):
        q, fields = {}, {**cls.model_fields}
        for k, v in request.query_params.items():
            q[f'{k}?contains'] = v.lower()
        return q
    
    @classmethod
    def query_from_dict(cls, data: dict):
        q, fields = {}, {**cls.model_fields}
        if data:
            for k, f in fields.items():
                if k in data.keys():
                    if f.annotation in [str, list[str]]:
                        q[f'{k}?contains'] = data[k]
        return q
        

        
    
    
