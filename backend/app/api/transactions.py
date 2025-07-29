from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from uuid import UUID

from ..database import get_db
from ..models import User, Transaction
from ..schemas import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionFilter,
    TransactionAnalytics
)
from ..services.auth import get_current_active_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    type: Optional[str] = None,
    min_amount: Optional[Decimal] = Query(None, ge=0),
    max_amount: Optional[Decimal] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List user transactions with optional filters.
    
    Args:
        start_date: Filter transactions after this date
        end_date: Filter transactions before this date
        category: Filter by category
        type: Filter by transaction type
        min_amount: Minimum transaction amount
        max_amount: Maximum transaction amount
        skip: Number of items to skip (pagination)
        limit: Number of items to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of transactions
    """
    # Build query
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    # Apply filters
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    if category:
        query = query.filter(Transaction.category == category.lower())
    
    if type:
        query = query.filter(Transaction.type == type.lower())
    
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)
    
    # Order by date descending
    query = query.order_by(Transaction.date.desc())
    
    # Apply pagination
    transactions = query.offset(skip).limit(limit).all()
    
    return transactions


@router.get("/analytics", response_model=TransactionAnalytics)
async def get_transaction_analytics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get transaction analytics for the current user.
    
    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Transaction analytics
    """
    # Default to last 30 days if no dates provided
    if not end_date:
        end_date = datetime.now(timezone.utc)
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Base query
    base_query = db.query(Transaction).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    )
    
    # Get total spent and count
    totals = db.query(
        func.sum(Transaction.amount).label('total'),
        func.count(Transaction.id).label('count')
    ).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).first()
    
    total_spent = Decimal(str(totals.total or 0))
    transaction_count = totals.count or 0
    average_transaction = total_spent / transaction_count if transaction_count > 0 else Decimal('0')
    
    # Get spending by category
    category_spending = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total')
    ).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).group_by(Transaction.category).all()
    
    by_category = {cat: Decimal(str(total)) for cat, total in category_spending}
    
    # Get spending by type
    type_spending = db.query(
        Transaction.type,
        func.sum(Transaction.amount).label('total')
    ).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).group_by(Transaction.type).all()
    
    by_type = {t: Decimal(str(total)) for t, total in type_spending}
    
    # Get spending trend (daily for last 30 days or less)
    daily_spending = db.query(
        func.date(Transaction.date).label('day'),
        func.sum(Transaction.amount).label('total')
    ).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).group_by(
        func.date(Transaction.date)
    ).order_by(
        func.date(Transaction.date)
    ).all()
    
    spending_trend = [
        {"date": str(day), "amount": float(total)}
        for day, total in daily_spending
    ]
    
    # Find most frequent and expensive categories
    most_frequent_category = None
    most_expensive_category = None
    
    if category_spending:
        # Most frequent (by count)
        category_counts = db.query(
            Transaction.category,
            func.count(Transaction.id).label('count')
        ).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.date >= start_date,
                Transaction.date <= end_date
            )
        ).group_by(Transaction.category).order_by(
            func.count(Transaction.id).desc()
        ).first()
        
        if category_counts:
            most_frequent_category = category_counts[0]
        
        # Most expensive (by total amount)
        sorted_categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
        if sorted_categories:
            most_expensive_category = sorted_categories[0][0]
    
    return TransactionAnalytics(
        total_spent=total_spent,
        average_transaction=average_transaction,
        transaction_count=transaction_count,
        by_category=by_category,
        by_type=by_type,
        spending_trend=spending_trend,
        most_frequent_category=most_frequent_category,
        most_expensive_category=most_expensive_category
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific transaction.
    
    Args:
        transaction_id: Transaction ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Transaction details
        
    Raises:
        HTTPException: If transaction not found or not owned by user
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new transaction.
    
    Args:
        transaction_data: Transaction data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created transaction
    """
    new_transaction = Transaction(
        user_id=current_user.id,
        type=transaction_data.type.lower(),
        amount=transaction_data.amount,
        date=transaction_data.date,
        category=transaction_data.category.lower(),
        location=transaction_data.location,
        description=transaction_data.description
    )
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    # TODO: In Phase 5, trigger AI analysis here
    # ai_engine.analyze_new_transaction(new_transaction)
    
    return new_transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: UUID,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a transaction.
    
    Args:
        transaction_id: Transaction ID
        transaction_data: Update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated transaction
        
    Raises:
        HTTPException: If transaction not found or not owned by user
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Update fields
    update_dict = transaction_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        if field in ["type", "category"] and value is not None:
            value = value.lower()
        setattr(transaction, field, value)
    
    db.commit()
    db.refresh(transaction)
    
    return transaction


@router.delete("/{transaction_id}", response_model=Dict[str, str])
async def delete_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a transaction.
    
    Args:
        transaction_id: Transaction ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If transaction not found or not owned by user
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    db.delete(transaction)
    db.commit()
    
    return {"message": "Transaction deleted successfully"}


@router.post("/bulk", response_model=List[TransactionResponse])
async def create_bulk_transactions(
    transactions: List[TransactionCreate],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create multiple transactions at once.
    
    Args:
        transactions: List of transaction data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of created transactions
    """
    if len(transactions) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 transactions can be created at once"
        )
    
    created_transactions = []
    
    for transaction_data in transactions:
        new_transaction = Transaction(
            user_id=current_user.id,
            type=transaction_data.type.lower(),
            amount=transaction_data.amount,
            date=transaction_data.date,
            category=transaction_data.category.lower(),
            location=transaction_data.location,
            description=transaction_data.description
        )
        db.add(new_transaction)
        created_transactions.append(new_transaction)
    
    db.commit()
    
    # Refresh all transactions
    for transaction in created_transactions:
        db.refresh(transaction)
    
    return created_transactions