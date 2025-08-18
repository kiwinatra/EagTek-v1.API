s='message'
r='sub'
q='Bearer'
p='WWW-Authenticate'
o='input'
n='status'
m=False
l='items'
k=Exception
W='*'
O=int
L=None
D=True
A=str
import logging as t
from typing import Optional as P,List as X,Dict as Q,Any as R
from datetime import datetime as G,timedelta as Y
import time as S,uuid,json
from fastapi import FastAPI as u,Depends as C,HTTPException as I,status as Z,Request,BackgroundTasks
from fastapi.security import OAuth2PasswordBearer as v,OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware as w
from fastapi.responses import JSONResponse as a
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as J,Field as b,EmailStr as x,validator as y
from passlib.context import CryptContext as z
from jose import JWTError as A0,jwt
from sqlalchemy import create_engine as A1,Column as F,Integer as T,String as M,Boolean,DateTime as c,ForeignKey as A2
from sqlalchemy.ext.declarative import declarative_base as A3
from sqlalchemy.orm import sessionmaker as A4,Session,relationship as d
from redis import Redis
import aioredis as A5
from celery import Celery
import httpx
class A6(J):API_V1_STR:A='/api/v1';PROJECT_NAME:A='Enterprise API';SECRET_KEY:A='your-secret-key-here';ALGORITHM:A='HS256';ACCESS_TOKEN_EXPIRE_MINUTES:O=30;DATABASE_URL:A='sqlite:///./sql_app.db';REDIS_URL:A='redis://localhost:6379';CELERY_BROKER_URL:A='redis://localhost:6379/0'
B=A6()
E=u(title=B.PROJECT_NAME,description='Сложный API сервер с аутентификацией, БД и фоновыми задачами',version='1.0.0',openapi_url=f"{B.API_V1_STR}/openapi.json")
E.add_middleware(w,allow_origins=[W],allow_credentials=D,allow_methods=[W],allow_headers=[W])
U=A3()
class H(U):__tablename__='users';id=F(T,primary_key=D,index=D);email=F(M,unique=D,index=D);hashed_password=F(M);is_active=F(Boolean,default=D);created_at=F(c,default=G.utcnow);items=d('Item',back_populates='owner')
class V(U):__tablename__=l;id=F(T,primary_key=D,index=D);title=F(M,index=D);description=F(M,index=D);owner_id=F(T,A2('users.id'));created_at=F(c,default=G.utcnow);owner=d('User',back_populates=l)
e=A1(B.DATABASE_URL)
A7=A4(autocommit=m,autoflush=m,bind=e)
U.metadata.create_all(bind=e)
A8=Redis.from_url(B.REDIS_URL)
A9=Celery(__name__,broker=B.CELERY_BROKER_URL)
@A9.task
def AA(data):S.sleep(10);return{'result':f"Processed {data[o]}",n:'completed'}
class AB(J):access_token:A;token_type:A
class AC(J):email:P[A]=L
class f(J):email:x
class AI(f):password:A
class g(f):
	id:O;is_active:bool;created_at:G
	class Config:orm_mode=D
class h(J):title:A;description:P[A]=L
class AJ(h):0
class i(h):
	id:O;owner_id:O;created_at:G
	class Config:orm_mode=D
class AK(J):
	transaction_id:A=b(default_factory=lambda:A(uuid.uuid4()));timestamp:G=b(default_factory=G.utcnow);user_data:Q[A,R];items:X[Q[A,R]];metadata:P[Q[A,R]]=L
	@y('user_data')
	def validate_user_data(cls,v):
		if not v.get('email'):raise ValueError('Email is required in user_data')
		return v
j=z(schemes=['bcrypt'],deprecated='auto')
AD=v(tokenUrl=f"{B.API_V1_STR}/token")
def AE(plain_password,hashed_password):return j.verify(plain_password,hashed_password)
def AF(password):return j.hash(password)
def AG(data,expires_delta=L):
	A=expires_delta;C=data.copy()
	if A:D=G.utcnow()+A
	else:D=G.utcnow()+Y(minutes=15)
	C.update({'exp':D});E=jwt.encode(C,B.SECRET_KEY,algorithm=B.ALGORITHM);return E
async def AL():return await A5.from_url(B.REDIS_URL)
def K():
	A=A7()
	try:yield A
	finally:A.close()
async def AH(token=C(AD),db=C(K)):
	A=I(status_code=Z.HTTP_401_UNAUTHORIZED,detail='Could not validate credentials',headers={p:q})
	try:
		E=jwt.decode(token,B.SECRET_KEY,algorithms=[B.ALGORITHM]);C=E.get(r)
		if C is L:raise A
		F=AC(email=C)
	except A0:raise A
	D=db.query(H).filter(H.email==F.email).first()
	if D is L:raise A
	return D
async def N(current_user=C(AH)):
	A=current_user
	if not A.is_active:raise I(status_code=400,detail='Inactive user')
	return A
@E.post(f"{B.API_V1_STR}/token",response_model=AB)
async def AM(form_data=C(),db=C(K)):
	C=form_data;A=db.query(H).filter(H.email==C.username).first()
	if not A or not AE(C.password,A.hashed_password):raise I(status_code=Z.HTTP_401_UNAUTHORIZED,detail='Incorrect username or password',headers={p:q})
	D=Y(minutes=B.ACCESS_TOKEN_EXPIRE_MINUTES);E=AG(data={r:A.email},expires_delta=D);return{'access_token':E,'token_type':'bearer'}
@E.post(f"{B.API_V1_STR}/users/",response_model=g)
def AN(user,db=C(K)):
	B=user;A=db.query(H).filter(H.email==B.email).first()
	if A:raise I(status_code=400,detail='Email already registered')
	C=AF(B.password);A=H(email=B.email,hashed_password=C);db.add(A);db.commit();db.refresh(A);return A
@E.get(f"{B.API_V1_STR}/users/me/",response_model=g)
async def AO(current_user=C(N)):return current_user
@E.post(f"{B.API_V1_STR}/items/",response_model=i)
def AP(item,current_user=C(N),db=C(K)):A=V(**item.dict(),owner_id=current_user.id);db.add(A);db.commit();db.refresh(A);return A
@E.get(f"{B.API_V1_STR}/items/",response_model=X[i])
def AQ(skip=0,limit=100,current_user=C(N),db=C(K)):A=db.query(V).filter(V.owner_id==current_user.id).offset(skip).limit(limit).all();return A
@E.post(f"{B.API_V1_STR}/complex-operation/")
async def AR(data,background_tasks,current_user=C(N),db=C(K)):
	E='transaction_id';B=data
	try:
		F=f"complex_op:{B.transaction_id}";await A8.set(F,json.dumps(B.dict()),ex=3600);background_tasks.add_task(AA,{o:B.transaction_id,'user_id':current_user.id})
		async with httpx.AsyncClient()as G:C=await G.post('https://api.eaglercraft.com/validate',json={E:B.transaction_id});C.raise_for_status()
		return{n:'processing',E:B.transaction_id,'timestamp':B.timestamp,'external_api_response':C.json()}
	except k as D:t.error(f"Complex operation failed: {A(D)}");raise I(status_code=500,detail=A(D))
@E.middleware('http')
async def AS(request,call_next):C=S.time();B=await call_next(request);D=S.time()-C;B.headers['X-Process-Time']=A(D);return B
@E.exception_handler(I)
async def AT(request,exc):return a(status_code=exc.status_code,content={s:exc.detail})
@E.exception_handler(k)
async def AU(request,exc):return a(status_code=500,content={s:'Internal server error'})
if __name__=='__main__':import uvicorn;uvicorn.run(E,host='0.0.0.0',port=8000,log_level='info')