from fastapi import APIRouter
from app.api.v1.auth.router import router as auth_router
from app.api.v1.employees.router import router as employees_router
from app.api.v1.salary.router import router as salary_router
from app.api.v1.deductions.router import router as deductions_router
from app.api.v1.tax.router import router as tax_router
from app.api.v1.payroll.router import router as payroll_router
from app.api.v1.payslips.router import router as payslips_router
from app.api.v1.exports.router import router as exports_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(employees_router, prefix="/employees", tags=["employees"])
api_router.include_router(salary_router, prefix="/salary-structures", tags=["salary_structures"])
api_router.include_router(deductions_router, prefix="/deductions", tags=["deductions"])
api_router.include_router(tax_router, prefix="/tax", tags=["tax"])
api_router.include_router(payroll_router, prefix="/payroll", tags=["payroll"])
api_router.include_router(payslips_router, prefix="/payslips", tags=["payslips"])
api_router.include_router(exports_router, prefix="/exports", tags=["exports"])
