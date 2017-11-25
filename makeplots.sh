#!/bin/sh


python makehistos.py met 300 0 30 mu
python drawhistos.py mu met met
python makehistos.py met 300 0 30 e
python drawhistos.py e met met
python makehistos.py met 300 0 30 di
python drawhistos.py di met met

python makehistos.py pt_1 300 0 30 mu
python drawhistos.py mu pt_1 pt_1
python makehistos.py pt_1 300 0 30 e
python drawhistos.py e pt_1 pt_1
python makehistos.py pt_1 300 0 30 di
python drawhistos.py di pt_1 pt_1

python makehistos.py pt_2 200 0 30 mu
python drawhistos.py mu pt_2 pt_2
python makehistos.py pt_2 200 0 30 e
python drawhistos.py e pt_2 pt_2
python makehistos.py pt_2 200 0 30 di
python drawhistos.py di pt_2 pt_2

python makehistos.py dR 2.5 0 20 mu
python drawhistos.py mu dR dR
python makehistos.py dR 2.5 0 20 e
python drawhistos.py e dR dR
python makehistos.py dR 2.5 0 20 di
python drawhistos.py di dR dR


python makehistos.py m_vis 130 0 30 mu
python drawhistos.py mu m_vis m_vis
python makehistos.py m_vis 130 0 30 e
python drawhistos.py e m_vis m_vis
python makehistos.py m_vis 130 0 30 di
python drawhistos.py di m_vis m_vis

python makehistos.py mt12 300 0 30 mu
python drawhistos.py mu mt12 mt12
python makehistos.py mt12 300 0 30  e
python drawhistos.py e mt12 mt12
python makehistos.py mt12 300 0 30 di
python drawhistos.py di mt12 mt12

python makehistos.py mt_1 200 0 30 mu
python drawhistos.py mu mt_1 mt_1
python makehistos.py mt_1 200 0 30 e
python drawhistos.py e mt_1 mt_1
python makehistos.py mt_1 200 0 30 di
python drawhistos.py di mt_1 mt_1

python makehistos.py mt_2 200 0 30 mu
python drawhistos.py mu mt_2 mt_2
python makehistos.py mt_2 200 0 30 e
python drawhistos.py e mt_2 mt_2
python makehistos.py mt_2 200 0 30 di
python drawhistos.py di mt_2 mt_2

python makehistos.py pth 300 0 30 mu
python drawhistos.py mu pth pth
python makehistos.py pth 300 0 30 e
python drawhistos.py e pth pth
python makehistos.py pth 300 0 30 di
python drawhistos.py di pth pth

python makehistos.py mt_1 200 0 30 mu
python drawhistos.py mu mt_1 mt_1
python makehistos.py mt_1 200 0 30 e
python drawhistos.py e mt_1 mt_1
python makehistos.py mt_1 200 0 30 di
python drawhistos.py di mt_1 mt_1

python makehistos.py eta_1 -3 3 30 mu
python drawhistos.py mu eta_1 eta_1
python makehistos.py eta_1 -3 3 30 e
python drawhistos.py e eta_1 eta_1
python makehistos.py eta_1 -3 3 30 di
python drawhistos.py di eta_1 eta_1

python makehistos.py eta_2 -3 3 30 mu
python drawhistos.py mu eta_2 eta_2
python makehistos.py eta_2 -3 3 30 e
python drawhistos.py e eta_2 eta_2
python makehistos.py eta_2 -3 3 30 di
python drawhistos.py di eta_2 eta_2

python makehistos.py phi_1 -3 3 20 mu
python drawhistos.py mu phi_1 phi_1
python makehistos.py phi_1 -3 3 20 e
python drawhistos.py e phi_1 phi_1
python makehistos.py phi_1 -3 3 20 di
python drawhistos.py di phi_1 phi_1

python makehistos.py phi_2 -3 3 20 mu
python drawhistos.py mu phi_2 phi_2
python makehistos.py phi_2 -3 3 20 e
python drawhistos.py e phi_2 phi_2
python makehistos.py phi_2 -3 3 20 di
python drawhistos.py di phi_2 phi_2













