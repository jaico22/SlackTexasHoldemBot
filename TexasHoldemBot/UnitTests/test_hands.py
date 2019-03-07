import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hand import Hand

testHand = Hand()

## Royal Flush
testHand.add_card(14,0)
testHand.add_card(10,0)
testHand.add_card(12,0)
testHand.add_card(11,0)
testHand.add_card(13,0)
testHand.clear()

## Straight Flush
testHand.add_card(9,3)
testHand.add_card(10,3)
testHand.add_card(12,3)
testHand.add_card(11,3)
testHand.add_card(13,3)
testHand.clear()

## Straight 
testHand.add_card(9,1)
testHand.add_card(10,2)
testHand.add_card(12,0)
testHand.add_card(11,3)
testHand.add_card(13,2)
testHand.clear()


## Flush
testHand.add_card(9,3)
testHand.add_card(2,3)
testHand.add_card(4,3)
testHand.add_card(11,3)
testHand.add_card(13,3)
testHand.clear()

## 4 of a kind - 1
testHand.add_card(14,3)
testHand.add_card(14,3)
testHand.add_card(14,0)
testHand.add_card(14,1)
testHand.add_card(2,3)
testHand.clear()

## 4 of a kind - 2
testHand.add_card(4,3)
testHand.add_card(4,3)
testHand.add_card(4,0)
testHand.add_card(4,1)
testHand.add_card(2,3)
testHand.clear()

## 3 of a kind 1
testHand.add_card(10,1)
testHand.add_card(10,3)
testHand.add_card(10,2)
testHand.add_card(1,3)
testHand.add_card(2,0)
testHand.clear()

## 3 of a kind 2
testHand.add_card(4,1)
testHand.add_card(4,3)
testHand.add_card(4,2)
testHand.add_card(7,3)
testHand.add_card(14,0)
testHand.clear()

## Full House
testHand.add_card(14,2)
testHand.add_card(14,3)
testHand.add_card(14,1)
testHand.add_card(10,3)
testHand.add_card(10,2)
testHand.clear()

## Full House - 2
testHand.add_card(2,2)
testHand.add_card(2,3)
testHand.add_card(2,1)
testHand.add_card(10,3)
testHand.add_card(10,2)
testHand.clear()

## 2 pair 1
testHand.add_card(14,3)
testHand.add_card(14,2)
testHand.add_card(7,2)
testHand.add_card(7,1)
testHand.add_card(2,3)
testHand.clear()

## 2 pair 1 Secondary TB
testHand.add_card(14,3)
testHand.add_card(14,2)
testHand.add_card(8,2)
testHand.add_card(8,1)
testHand.add_card(2,3)
testHand.clear()

## 1 pair
testHand.add_card(9,3)
testHand.add_card(9,2)
testHand.add_card(5,1)
testHand.add_card(14,0)
testHand.add_card(2,3)
testHand.clear()